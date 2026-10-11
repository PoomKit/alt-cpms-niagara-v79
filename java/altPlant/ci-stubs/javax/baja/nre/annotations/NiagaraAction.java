package javax.baja.nre.annotations;
import java.lang.annotation.*;
@Retention(RetentionPolicy.SOURCE) @Target(ElementType.TYPE) @Repeatable(NiagaraActions.class)
public @interface NiagaraAction { String name(); String parameterType() default ""; String defaultValue() default ""; String returnType() default ""; int flags() default 0; }
