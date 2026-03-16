package graalpy.demo;

import io.micronaut.http.HttpRequest;
import io.micronaut.http.MediaType;
import io.micronaut.http.client.HttpClient;
import io.micronaut.http.client.annotation.Client;
import io.micronaut.http.client.multipart.MultipartBody;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertEquals;

@MicronautTest
final class ReviewControllerTest {
    @Inject
    @Client("/")
    HttpClient httpClient;

    @Test
    void analyzeEndpointAcceptsAReviewUpload() {
        MultipartBody body = MultipartBody.builder()
            .addPart(
                "file",
                "review.txt",
                MediaType.TEXT_PLAIN_TYPE,
                """
                    This monitor looks great, setup was easy, and the screen is bright and sharp.
                    """.getBytes(StandardCharsets.UTF_8)
            )
            .build();

        HttpRequest<?> request = HttpRequest.POST("/api/reviews/analyze", body)
            .contentType(MediaType.MULTIPART_FORM_DATA_TYPE);

        ReviewAnalysisView response = httpClient.toBlocking().retrieve(request, ReviewAnalysisView.class);
        assertEquals("review.txt", response.fileName());
        assertEquals("Positive", response.sentiment().label());
    }
}
