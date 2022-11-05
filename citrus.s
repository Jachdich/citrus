.text
.globl add
.type add, @function
.globl add_maybe
.type add_maybe, @function
.globl main
.type main, @function
add:
	pushq	%rbp                                    ; 235
	movq	%rsp,	%rbp
	subq	$16,	%rsp
	movq	%rdi,	-0(%rbp)                        ; 242
	movq	%rsi,	-8(%rbp)                        ; 242
	movq	-0(%rbp),	%rax                    ; 203
	movq	-8(%rbp),	%rcx                    ; 203
	addq	%rax,	%rcx                            ; 185
	movq	%rcx,	%rax                            ; 256
	leave                                           ; 259
	ret                                             ; 260
add_maybe:
	pushq	%rbp                                    ; 235
	movq	%rsp,	%rbp
	subq	$16,	%rsp
	movq	%rdi,	-0(%rbp)                        ; 242
	movq	%rsi,	-8(%rbp)                        ; 242
	pushq	%rcx                                    ; 158
	movq	-0(%rbp),	%rax                    ; 203
	movq	%rax,	%rdi                            ; 164
	call	putd                                    ; 167
	movq	%rax,	%rax                            ; 170
	popq	%rcx                                    ; 173
	pushq	%rcx                                    ; 158
	movq	-8(%rbp),	%rax                    ; 203
	movq	%rax,	%rdi                            ; 164
	call	putd                                    ; 167
	movq	%rax,	%rax                            ; 170
	popq	%rcx                                    ; 173
	pushq	%rcx                                    ; 158
	movq	-0(%rbp),	%rax                    ; 203
	movq	%rax,	%rdi                            ; 164
	movq	-8(%rbp),	%rax                    ; 203
	movq	%rax,	%rsi                            ; 164
	call	add                                     ; 167
	movq	%rax,	%rax                            ; 170
	popq	%rcx                                    ; 173
	movq	%rax,	%rax                            ; 256
	leave                                           ; 259
	ret                                             ; 260
main:
	pushq	%rax                                    ; 158
	pushq	%rcx                                    ; 158
	pushq	%rax                                    ; 158
	pushq	%rcx                                    ; 158
	movq	$1,	%rdx                            ; 192
	movq	%rdx,	%rdi                            ; 164
	movq	$1,	%rdx                            ; 192
	movq	%rdx,	%rsi                            ; 164
	call	add_maybe                               ; 167
	movq	%rax,	%rdx                            ; 170
	popq	%rax                                    ; 173
	popq	%rcx                                    ; 173
	movq	%rdx,	%rdi                            ; 164
	call	putd                                    ; 167
	movq	%rax,	%rdx                            ; 170
	popq	%rax                                    ; 173
	popq	%rcx                                    ; 173
	movq	$0,	%rdx                            ; 192
	movq	%rdx,	%rax                            ; 256
	ret                                             ; 260
