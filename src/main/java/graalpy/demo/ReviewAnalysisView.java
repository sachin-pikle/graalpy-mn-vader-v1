package graalpy.demo;

import io.micronaut.serde.annotation.Serdeable;

@Serdeable
public record ReviewAnalysisView(
    String fileName,
    SentimentScores sentiment
) {
    @Serdeable
    public record SentimentScores(
        double positive,
        double neutral,
        double negative,
        double compound,
        String label
    ) {
    }
}
