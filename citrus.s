.text
.globl putd
.type putd, @function
.globl main
.type main, @function
main:                                           # funcdef:368       []
    movq        $6,         %rdi                # int_literal:304   ['%rdi int_literal:303']
    movq        $10,        %rax                # int_literal:304   ['%rax int_literal:303', '%rdi int_literal:303']
    movq        %rax,       %rax                # binexpr:279       ['%rdi int_literal:303']
    cdq                                         # binexpr:280       ['%rdi int_literal:303']
    idivq       %rdi                            # binexpr:281       ['%rdi int_literal:303']
    movq        %rdx,       %rdi                # binexpr:285       ['%rdi int_literal:303']
    call        putd                            # funccall:209      []
    movq        $0,         %rax                # int_literal:304   ['%rax int_literal:303']
    ret                                         # funcdef:406       []
