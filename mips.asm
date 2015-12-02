.data
.text
.globl main

main:

li $a0, 2
sw $a0, 0($sp)
addiu $sp, $sp, -4

li $a0, 3
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp, 4
lw $t2, 4($sp)
addiu $sp, $sp, 4
add $a0, $t2, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

lw $t1, 4($sp)
addiu $sp, $sp 4
sub $a0, $t1, $t1
sub $a0, $a0, $t1
sw $a0, 0($sp)
addiu $sp, $sp, -4

li $v0, 1
syscall

li $v0, 10
syscall
