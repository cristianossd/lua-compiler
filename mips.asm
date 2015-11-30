.data
x: .word 0
.text
.globl main

main:

li $a0, 7
sw $a0, 0($sp)
addiu $sp, $sp, -4

li $a0, 5
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp, 4
lw $t2, 4($sp)
addiu $sp, $sp, 4
add $a0, $t2, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $a0, 4($sp)
addiu $sp, $sp 4
sw $a0, x

lw $a0, x
li $v0, 1
syscall

li $v0, 10
syscall
