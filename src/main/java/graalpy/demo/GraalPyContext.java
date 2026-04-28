package graalpy.demo;

import jakarta.annotation.PreDestroy;
import jakarta.inject.Singleton;
import org.graalvm.polyglot.Source;
import org.graalvm.polyglot.Value;
import org.graalvm.python.embedding.GraalPyResources;

@Singleton
public final class GraalPyContext {
    private final org.graalvm.polyglot.Context context;

    public GraalPyContext(
        @io.micronaut.context.annotation.Value("${graalpy.dap.enabled:false}") boolean dapEnabled
    ) {
        var contextBuilder = GraalPyResources.contextBuilder()
            .allowAllAccess(true)
            .allowExperimentalOptions(true);

        if (dapEnabled) {
            // The options below allow us to debug the Python code while running in Java.
            contextBuilder
                .option("dap", "localhost:4711")
                .option("dap.Suspend", "true")
                .option("dap.WaitAttached", "true");
        }

        this.context = contextBuilder.build();
    }

    public Value eval(Source source) {
        return context.eval(source);
    }

    public Value getMember(String name) {
        return context.getBindings("python").getMember(name);
    }

    @PreDestroy
    void close() {
        context.close(true);
    }
}
