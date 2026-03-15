package gids.graalpy.demo;

import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@MicronautTest
final class GraalPySentimentServiceTest {
    @Inject
    GraalPySentimentService graalPySentimentService;

    @Test
    void helloComesFromGraalPy() {
        HelloView hello = graalPySentimentService.hello();
        assertTrue(hello.message().contains("GraalPy"));
    }

    @Test
    void analyzesPositiveReview() {
        ReviewAnalysisView result = graalPySentimentService.analyze(
            "sample-review.txt",
            """
                I love these headphones. The battery life is fantastic and the sound is rich and clear.
                """.getBytes(StandardCharsets.UTF_8)
        );

        assertEquals("sample-review.txt", result.fileName());
        assertEquals("Positive", result.sentiment().label());
        assertTrue(result.sentiment().compound() > 0.05);
    }
}
