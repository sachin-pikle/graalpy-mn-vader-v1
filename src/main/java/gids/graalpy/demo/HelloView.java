package gids.graalpy.demo;

import io.micronaut.serde.annotation.Serdeable;

@Serdeable
public record HelloView(String message) {
}
