# pylint: disable=missing-docstring


def sudoku_validator(grid):

    correct_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 1. التأكد من كل صف
    for row in grid:
        if sorted(row) != correct_numbers:
            return False

    # 2. التأكد من كل عمود
    for col_index in range(9):
        column = []
        for row_index in range(9):
            column.append(grid[row_index][col_index])
        if sorted(column) != correct_numbers:
            return False

    # 3. التأكد من الصناديق الصغيرة (3x3)
    for start_row in [0, 3, 6]:
        for start_col in [0, 3, 6]:
            box = []
            # نجمع الـ 9 أرقام داخل الصندوق الصغير
            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    box.append(grid[r][c])

            if sorted(box) != correct_numbers:
                return False

    # إذا فحصنا كل شيء وما كان فيه أي خطأ
    return True
