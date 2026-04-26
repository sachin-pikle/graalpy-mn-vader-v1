package graalpy.demo;

import io.micronaut.core.io.ResourceResolver;
import io.micronaut.json.JsonMapper;
import jakarta.inject.Singleton;
import org.graalvm.polyglot.Context;
import org.graalvm.polyglot.Source;
import org.graalvm.python.embedding.GraalPyResources;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.URL;
import java.nio.charset.StandardCharsets;

@Singleton
public final class GraalPySentimentService {
    private static final Logger LOG = LoggerFactory.getLogger(GraalPySentimentService.class);
    private static final String SCRIPT_PATH = "classpath:org.graalvm.python.vfs/src/sentiment_app.py";

    private final JsonMapper jsonMapper;
    private final Source sentimentAppSource;

    public GraalPySentimentService(JsonMapper jsonMapper, ResourceResolver resourceResolve) throws IOException{
        this.jsonMapper = jsonMapper;
        URL sentimentAppURL = resourceResolve.getResource(SCRIPT_PATH).get();
        sentimentAppSource = Source.newBuilder("python", sentimentAppURL).build();

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
                    // .option("engine.WarnVirtualThreadSupport", "false") // experimental: Suppress log warnings
                    // The options below allow us to debug the Python code while running in Java
                    .option("dap", "localhost:4711")
                    .option("dap.Suspend", "true")
                    .option("dap.WaitAttached", "true")
                    .build()) {
            context.eval(sentimentAppSource);
            var function = context.getBindings("python").getMember("analyze_review_json");
            if (function == null || !function.canExecute()) {
                throw new IllegalStateException("Python analysis function is not available.");
            }
            return function.execute(fileName, reviewText).asString();
        }
    }
}
