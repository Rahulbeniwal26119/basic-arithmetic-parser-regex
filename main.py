from parser import Parser
parser = Parser()

test = [
    ('1 + 2', 3),
    (' 2 * 2 + 3', 7),
    (' 10 * ( 5 * 6 ) + 7', 307),
    ('11 - 11 * 20', -209),
    ('(2 - 2 ) * 10', 0)
]

result_set = []
for expr, expected_result in test:
    result = parser.parse(expr)
    result_set.append(result == expected_result)

if all(result_set):
    print('All tests passed')
else:
    print('Some tests failed')
