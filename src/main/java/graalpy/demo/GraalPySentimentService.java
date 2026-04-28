package graalpy.demo;

import io.micronaut.core.io.ResourceResolver;
import io.micronaut.json.JsonMapper;
import jakarta.inject.Singleton;
import org.graalvm.polyglot.Source;
import org.graalvm.polyglot.Value;
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
    private final Value analyzeReviewJson;

    public GraalPySentimentService(
        JsonMapper jsonMapper,
        GraalPyContext graalPyContext,
        ResourceResolver resourceResolver
    ) throws IOException {
        this.jsonMapper = jsonMapper;

        URL sentimentAppURL = resourceResolver.getResource(SCRIPT_PATH).orElseThrow();
        Source sentimentAppSource = Source.newBuilder("python", sentimentAppURL).build();
        graalPyContext.eval(sentimentAppSource);
        this.analyzeReviewJson = graalPyContext.getMember("analyze_review_json");
        if (analyzeReviewJson == null || !analyzeReviewJson.canExecute()) {
            throw new IllegalStateException("Python analysis function is not available.");
        }
    }

    public ReviewAnalysisView analyze(String fileName, byte[] fileBytes) {
        String reviewText = new String(fileBytes, StandardCharsets.UTF_8).trim();
        LOG.info("Running GraalPy VADER analysis for {}", fileName);
        String payload = analyzeReviewJson.execute(fileName, reviewText).asString();
        try {
            return jsonMapper.readValue(payload.getBytes(StandardCharsets.UTF_8), ReviewAnalysisView.class);
        } catch (IOException e) {
            throw new IllegalStateException("Unable to parse GraalPy sentiment response.", e);
        }
    }
}
