from diffeq.utils.symbolic import *
x, y = variable('x'), variable('y')
expression = x**2 + y*x + cos(x) + 3

print(expression)

print('без оптимизаций:')
print(expression.diff('x'))
print(expression.diff('y'))
print('с оптимизациями:')

print(expression.diff('x').optim())
print(expression.diff('y').optim())

print('дважды производная:')
print(expression.diff('x').diff('x').optim())


print('упаковка в "программы"')

prog = program({'output':expression})
prog(x = 1, y = 2)


print('порядок выполнения:')
print(prog)