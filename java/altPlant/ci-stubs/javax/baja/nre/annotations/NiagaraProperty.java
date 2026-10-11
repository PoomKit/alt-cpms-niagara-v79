package javax.baja.nre.annotations;
import java.lang.annotation.*;
@Retention(RetentionPolicy.SOURCE) @Target(ElementType.TYPE) @Repeatable(NiagaraProperties.class)
public @interface NiagaraProperty { String name(); String type(); String defaultValue(); int flags() default 0; }
