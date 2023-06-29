# content of test_demo1.py
class TestDemo1:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert not hasattr(x, "check")