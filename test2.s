.text
.global main
.type main, @function
main:
pushq %rdi
pushq %rax
movq $1, %rbx
movq %rbx, %rdi
movq $1, %rbx
movq %rbx, %rsi
call add
movq %rax, %rbx
popq %rax
popq %rdi
movq %rbx, %rdi
call putd
movq %rax, %rbx
ret

add:
addq %rdi, %rsi
movq %rsi, %rax
ret
