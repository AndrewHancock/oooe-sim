testFunction(int*, int):
        sub     sp, sp, #32
        str     x0, [sp, 8]
        str     w1, [sp, 4]
        str     wzr, [sp, 28]
        str     wzr, [sp, 24]
        b       .L2
.L3:
        ldrsw   x0, [sp, 24]
        lsl     x0, x0, 2
        ldr     x1, [sp, 8]
        add     x0, x1, x0
        ldr     w0, [x0]
        ldr     w1, [sp, 28]
        add     w0, w1, w0
        str     w0, [sp, 28]
        ldr     w0, [sp, 24]
        add     w0, w0, 1
        str     w0, [sp, 24]
.L2:
        ldr     w1, [sp, 24]
        ldr     w0, [sp, 4]
        cmp     w1, w0
        blt     .L3
        ldr     w0, [sp, 28]
        add     sp, sp, 32
        ret