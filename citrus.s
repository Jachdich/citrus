.text
.globl add
.type add, @function
.globl add_maybe
.type add_maybe, @function
.globl main
.type main, @function
add:
	pushq	%rbp                                    # 235	[]
	movq	%rsp,	%rbp
	subq	$16,	%rsp
	movq	%rdi,	-0(%rbp)                        # 242	[]
	movq	%rsi,	-8(%rbp)                        # 242	[]
	movq	-0(%rbp),	%rax                    # 203	['%rax']
	movq	-8(%rbp),	%rcx                    # 203	['%rax', '%rcx']
	addq	%rax,	%rcx                            # 185	['%rax', '%rcx']
	movq	%rcx,	%rax                            # 256	['%rcx']
	leave                                           # 259	['%rcx']
	ret                                             # 260	['%rcx']
add_maybe:
	pushq	%rbp                                    # 235	['%rcx']
	movq	%rsp,	%rbp
	subq	$16,	%rsp
	movq	%rdi,	-0(%rbp)                        # 242	['%rcx']
	movq	%rsi,	-8(%rbp)                        # 242	['%rcx']
	pushq	%rcx                                    # 158	['%rcx']
	movq	-0(%rbp),	%rax                    # 203	['%rax', '%rcx']
	movq	%rax,	%rdi                            # 164	['%rax', '%rcx']
	call	putd                                    # 167	['%rcx']
	movq	%rax,	%rax                            # 170	['%rax', '%rcx']
	popq	%rcx                                    # 173	['%rax', '%rcx']
	pushq	%rcx                                    # 158	['%rcx']
	movq	-8(%rbp),	%rax                    # 203	['%rax', '%rcx']
	movq	%rax,	%rdi                            # 164	['%rax', '%rcx']
	call	putd                                    # 167	['%rcx']
	movq	%rax,	%rax                            # 170	['%rax', '%rcx']
	popq	%rcx                                    # 173	['%rax', '%rcx']
	pushq	%rcx                                    # 158	['%rcx']
	movq	-0(%rbp),	%rax                    # 203	['%rax', '%rcx']
	movq	%rax,	%rdi                            # 164	['%rax', '%rcx']
	movq	-8(%rbp),	%rax                    # 203	['%rax', '%rcx']
	movq	%rax,	%rsi                            # 164	['%rax', '%rcx']
	call	add                                     # 167	['%rcx']
	movq	%rax,	%rax                            # 170	['%rax', '%rcx']
	popq	%rcx                                    # 173	['%rax', '%rcx']
	movq	%rax,	%rax                            # 256	['%rax', '%rcx']
	leave                                           # 259	['%rax', '%rcx']
	ret                                             # 260	['%rax', '%rcx']
main:
	pushq	%rax                                    # 158	['%rax', '%rcx']
	pushq	%rcx                                    # 158	['%rax', '%rcx']
	pushq	%rax                                    # 158	['%rax', '%rcx']
	pushq	%rcx                                    # 158	['%rax', '%rcx']
	movq	$1,	%rdx                            # 192	['%rax', '%rcx', '%rdx']
	movq	%rdx,	%rdi                            # 164	['%rax', '%rcx', '%rdx']
	movq	$1,	%rdx                            # 192	['%rax', '%rcx', '%rdx']
	movq	%rdx,	%rsi                            # 164	['%rax', '%rcx', '%rdx']
	call	add_maybe                               # 167	['%rax', '%rcx']
	movq	%rax,	%rdx                            # 170	['%rax', '%rcx', '%rdx']
	popq	%rax                                    # 173	['%rax', '%rcx', '%rdx']
	popq	%rcx                                    # 173	['%rax', '%rcx', '%rdx']
	movq	%rdx,	%rdi                            # 164	['%rax', '%rcx', '%rdx']
	call	putd                                    # 167	['%rax', '%rcx']
	movq	%rax,	%rdx                            # 170	['%rax', '%rcx', '%rdx']
	popq	%rax                                    # 173	['%rax', '%rcx', '%rdx']
	popq	%rcx                                    # 173	['%rax', '%rcx', '%rdx']
	movq	$0,	%rdx                            # 192	['%rax', '%rcx', '%rdx']
	movq	%rdx,	%rax                            # 256	['%rax', '%rcx', '%rdx']
	ret                                             # 260	['%rax', '%rcx', '%rdx']
