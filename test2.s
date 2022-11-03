.text
.global main
.type main, @function
main:movq $1, %rax
movq $1, %rbx
addq %rax, %rbx
movq %rbx, %rdi
call putd
movq $6, %rax
movq $9, %rbx
imul %rax, %rbx
movq %rbx, %rdi
call putd
ret
