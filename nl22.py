#! /usr/bin/python3

import sys
import subprocess

stack = []

def push(x):
    stack.append(x)

def add(x):
	y = stack.pop()
	stack.append(y+x)
	return stack[-1]

def printStack():
    print((str(stack).replace("[", "")).replace("]", ""))

def sub(x):
	y = stack.pop()
	stack.append(y-x)
	return stack[-1]

def sim_mode(program):
    for op in program:
        exec(op)

def compile_prog(program, out_file):
    with open(out_file, w) as out:
        out.write("section .text\n")
        out.write("    global _start\n")
        out.write("_start:\n")
        for op in program:
            if "push(" in op:
                num = ""
                for a in op:
                    if a is not int:
                        continue
                    else: 
                        num += str(a)
                        continue
                out.write("push " + num)
        out.write("mov rax, 60")
        out.write("mov rdi, 0")
        out.write("syscall")

program = [
"push(59)",
"add(63)",
"add(5)",
"sub(7)",
"printStack()"
]

def usage():
	print("USAGE: nerd [SUBCOMMAND] [*ARGS]")
	print("SUBCOMMANDS:")
	print("    sim        Simulation mode (Interpret code)")
	print("    com        Compilation mode (Compile code)")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        print("ERROR: No subcommand given")
        exit(1)
    subcommand = sys.argv[1]

    if subcommand == "sim":
        sim_mode(program)
    elif subcommand == "com":
        compile_prog(program, "output.asm")
        subprocess.call(["nasm", "-f", "elf64", "output.asm"])
        subprocess.call(["ld", "-o", "output", "output.o"])
    else:
        usage()
        print("ERROR: Invalid subcommand")
        exit(1)
