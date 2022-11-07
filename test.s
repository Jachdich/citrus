	.file	"test.c"
	.text
	.globl	fn
	.type	fn, @function
fn:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	.cfi_offset 3, -24
	movq	%rax, %rsi
	movabsq	$-4294967296, %rcx
	andq	%rsi, %rcx
	orq	$1, %rcx
	movq	%rcx, %rax
	movq	%rax, %rcx
	movl	%ecx, %esi
	movabsq	$8589934592, %rcx
	orq	%rsi, %rcx
	movq	%rcx, %rax
	movq	%rdx, %rsi
	movabsq	$-4294967296, %rcx
	andq	%rsi, %rcx
	orq	$3, %rcx
	movq	%rcx, %rdx
	movq	%rdx, %rcx
	movl	%ecx, %esi
	movabsq	$17179869184, %rcx
	orq	%rsi, %rcx
	movq	%rcx, %rdx
	movq	-8(%rbp), %rbx
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	fn, .-fn
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	$0, %eax
	call	fn
	movq	%rax, -16(%rbp)
	movq	%rdx, -8(%rbp)
	movl	-16(%rbp), %edx
	movl	-12(%rbp), %eax
	addl	%eax, %edx
	movl	-8(%rbp), %eax
	addl	%eax, %edx
	movl	-4(%rbp), %eax
	addl	%edx, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.ident	"GCC: (GNU) 12.2.0"
	.section	.note.GNU-stack,"",@progbits
