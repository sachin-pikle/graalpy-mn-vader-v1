package graalpy.demo;

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
    void analyzesPositiveReview() {
        ReviewAnalysisView result = graalPySentimentService.analyze(
            "product-coffee-grinder-positive.txt",
            """
                I bought this coffee grinder last week and I am really happy with it.
                It feels solid, the grind is consistent, and setup took less than five minutes.
                The lid is a little noisy, but overall it feels like a great value.
                """.getBytes(StandardCharsets.UTF_8)
        );

        assertEquals("product-coffee-grinder-positive.txt", result.fileName());
        assertEquals("Positive", result.sentiment().label());
        assertTrue(result.sentiment().compound() > 0.05);
    }
}
