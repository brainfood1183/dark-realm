
num = -1845

if num == 0:
	print(0)
val = [10,11,12 ]
dict_val = {
	"10": "A",
	"11": "B",
	"12": "C"
}
string = ""

while num != 0:
	remainder = num % 13
	if remainder in val:
		string = string + dict_val[str(remainder)]
	else:
		string = string + str(remainder)
	num = num // 13
print(string[::-1])