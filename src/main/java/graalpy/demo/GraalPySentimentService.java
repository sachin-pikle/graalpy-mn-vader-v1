package graalpy.demo;

import io.micronaut.core.io.ResourceLoader;
import io.micronaut.json.JsonMapper;
import jakarta.inject.Singleton;
import org.graalvm.polyglot.Context;
import org.graalvm.polyglot.Source;
import org.graalvm.python.embedding.GraalPyResources;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

@Singleton
public final class GraalPySentimentService {
    private static final Logger LOG = LoggerFactory.getLogger(GraalPySentimentService.class);
    private static final String SCRIPT_PATH = "classpath:python/sentiment_app.py";

    private final JsonMapper jsonMapper;
    private final String pythonScript;

    public GraalPySentimentService(JsonMapper jsonMapper, ResourceLoader resourceLoader) {
        this.jsonMapper = jsonMapper;
        this.pythonScript = loadScript(resourceLoader);
    }

    public ReviewAnalysisView analyze(String fileName, byte[] fileBytes) {
        String reviewText = new String(fileBytes, StandardCharsets.UTF_8).trim();
        LOG.info("Running GraalPy VADER analysis for {}", fileName);
        String payload = runAnalysis(fileName, reviewText);
        try {
            return jsonMapper.readValue(payload.getBytes(StandardCharsets.UTF_8), ReviewAnalysisView.class);
        } catch (IOException e) {
            throw new IllegalStateException("Unable to parse GraalPy sentiment response.", e);
        }
    }

    private String runAnalysis(String fileName, String reviewText) {
        try (Context context = GraalPyResources.contextBuilder()
                    .allowAllAccess(true)
                    .allowExperimentalOptions(true)
                    .option("engine.WarnVirtualThreadSupport", "false") // experimental: Suppress log warnings
                    .build()) {
            context.eval(Source.newBuilder("python", pythonScript, "sentiment_app.py").buildLiteral());
            var function = context.getBindings("python").getMember("analyze_review_json");
            if (function == null || !function.canExecute()) {
                throw new IllegalStateException("Python analysis function is not available.");
            }
            return function.execute(fileName, reviewText).asString();
        }
    }

    private String loadScript(ResourceLoader resourceLoader) {
        try (InputStream stream = resourceLoader.getResourceAsStream(SCRIPT_PATH).orElseThrow()) {
            return new String(stream.readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException("Unable to load Python script " + SCRIPT_PATH, e);
        }
    }
}
