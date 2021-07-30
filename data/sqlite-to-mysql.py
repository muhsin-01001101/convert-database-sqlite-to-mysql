# LICENSED TO https://github.com/muhsin-01001101

import sys
import re

def main():
    print "SET sql_mode='NO_BACKSLASH_ESCAPES';"
    constraints = []
    lines = sys.stdin.read().splitlines()
    for line in lines:
        processLine(line, constraints)
    for constraint in constraints:
        print constraint

def processLine(line, constraints):
    if (
        line.startswith("PRAGMA") or
        line.startswith("BEGIN TRANSACTION;") or
        line.startswith("COMMIT;") or
        line.startswith("DELETE FROM sqlite_sequence;") or
        line.startswith("INSERT INTO \"sqlite_sequence\"")
       ):
        return
    line = line.replace("AUTOINCREMENT", "AUTO_INCREMENT")
    line = line.replace("NOT DEFERRABLE INITIALLY IMMEDIATE", "")
    line = line.replace("CLOB", "TEXT")
    line = line.replace("DEFAULT 't'", "DEFAULT '1'")
    line = line.replace("DEFAULT 'f'", "DEFAULT '0'")
    line = line.replace(",'t'", ",'1'")
    line = line.replace(",'f'", ",'0'")
    result = extractConstraint(line, constraints)
    while result != -1:
        line = result
        result = extractConstraint(line, constraints)
    in_string = False
    newLine = ''
    for c in line:
        if not in_string:
            if c == "'":
                in_string = True
            elif c == '"':
                newLine = newLine + '`'
                continue
        elif c == "'":
            in_string = False
        newLine = newLine + c
    print newLine

def extractConstraint(line, constraints):
    p = re.compile('CREATE TABLE (\w+) (.*), CONSTRAINT (\w+) FOREIGN KEY \((\w+)\) REFERENCES (\w+) \((\w+)\)( ON DELETE CASCADE)? (.*)')
    matches = p.findall(line)
    line = -1
    for match in matches:
        line = 'CREATE TABLE ' + match[0] + ' ' + match[1] + ' ' + match[len(match)-1]
        constraint = 'ALTER TABLE ' + match[0] + ' ADD CONSTRAINT ' + match[2] + ' FOREIGN KEY (' + match[3] + ') REFERENCES ' + match[4] + '(' + match[5] + ')'
        if len(match) == 8:
            constraint += match[6]
        constraints.append(constraint + ';')
    return line


if __name__ == "__main__":
    main()