package gids.graalpy.demo;

import io.micronaut.http.HttpResponse;
import io.micronaut.http.MediaType;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.Produces;
import io.micronaut.http.multipart.CompletedFileUpload;
import io.micronaut.scheduling.TaskExecutors;
import io.micronaut.scheduling.annotation.ExecuteOn;

import java.io.IOException;
import java.util.Map;

@Controller("/api")
final class ReviewController {
    private final GraalPySentimentService graalPySentimentService;

    ReviewController(GraalPySentimentService graalPySentimentService) {
        this.graalPySentimentService = graalPySentimentService;
    }

    @Get("/hello")
    @Produces(MediaType.APPLICATION_JSON)
    HelloView hello() {
        return graalPySentimentService.hello();
    }

    @Post(uri = "/reviews/analyze", consumes = MediaType.MULTIPART_FORM_DATA)
    @Produces(MediaType.APPLICATION_JSON)
    @ExecuteOn(TaskExecutors.BLOCKING)
    HttpResponse<?> analyze(CompletedFileUpload file) throws IOException {
        if (file == null || file.getFilename() == null || file.getFilename().isBlank()) {
            return HttpResponse.badRequest(Map.of("message", "Choose a review file before uploading."));
        }

        if (file.getSize() == 0) {
            return HttpResponse.badRequest(Map.of("message", "The uploaded file is empty."));
        }

        return HttpResponse.ok(graalPySentimentService.analyze(file.getFilename(), file.getBytes()));
    }
}
