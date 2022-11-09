.text
.globl putd
.type putd, @function
.globl main
.type main, @function
main:                                           # funcdef:444       []
    movq        $1000000,   %rax                # int_literal:389   ['%rax int_literal:388']
    movq        $10,        %rdi                # int_literal:389   ['%rax int_literal:388', '%rdi int_literal:388']
    cdq                                         # int_div:312       ['%rdi int_literal:388']
    idivq       %rdi                            # int_div:313       ['%rdi int_literal:388']
    movq        %rax,       %rdi                # int_div:317       ['%rdi int_literal:388']
    call        putd                            # funccall:263      []
    movq        $0,         %rax                # int_literal:389   ['%rax int_literal:388']
    ret                                         # funcdef:483       []
