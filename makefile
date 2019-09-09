vm: vm.c
	gcc vm.c -o vm -Wall

clean:
	rm -rf vm *~
