package javax.baja.nre.annotations;
import java.lang.annotation.*;
@Retention(RetentionPolicy.SOURCE) @Target(ElementType.TYPE) public @interface NiagaraProperties { NiagaraProperty[] value(); }
