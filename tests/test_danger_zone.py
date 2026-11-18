from monitoring.danger_zone import contains, parse_zone

def test_parse_zone(): assert parse_zone("0,0; 1,0; 0,1") == [(0.,0.),(1.,0.),(0.,1.)]
def test_centroid_inside_zone(): assert contains((40,40,60,60),[(0,0),(1,0),(1,1),(0,1)],100,100).inside
def test_centroid_outside_zone(): assert not contains((120,40,140,60),[(0,0),(1,0),(1,1),(0,1)],100,100).inside
