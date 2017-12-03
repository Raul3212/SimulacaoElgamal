def euclides(r0, r1):
	results = [min(r0, r1)]
	i = 0
	while not results[i] == 0:
		r0, r1 = max(r0,r1) % min(r0, r1), min(r0, r1)
		results.append(r0)
		i += 1
	return results[i-1]

def euclides_extendido(r0, r1):
	rs = [r0, r1]
	ss = [1, 0]
	ts = [0, 1]
	qs = [None]
	i = 1
	while not rs[i] == 0:
		i += 1
		rs.insert(i, rs[i-2] % rs[i-1])
		qs.insert(i-1, int((rs[i-2]-rs[i])/rs[i-1]))
		ss.insert(i, ss[i-2] - qs[i-1] * ss[i-1])
		ts.insert(i, ts[i-2] - qs[i-1] * ts[i-1])
	return (rs[i-1], ss[i-1], ts[i-1])


def main():
	print(euclides_extendido(49, 640))

if __name__ == '__main__':
	main()
