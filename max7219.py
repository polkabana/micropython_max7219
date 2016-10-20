# based on adafruit's code https://github.com/adafruit/micropython-adafruit-max7219/blob/master/max7219.py
#
_NOOP = const(0)
_DIGIT0 = const(1)
_DIGIT1 = const(2)
_DIGIT2 = const(3)
_DIGIT3 = const(4)
_DIGIT4 = const(5)
_DIGIT5 = const(6)
_DIGIT6 = const(7)
_DIGIT7 = const(8)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

_font = b'\x00\x00\x00\x00\x00\
\x00\x00\x5F\x00\x00\
\x00\x07\x00\x07\x00\
\x14\x7F\x14\x7F\x14\
\x24\x2A\x7F\x2A\x12\
\x23\x13\x08\x64\x62\
\x36\x49\x55\x22\x50\
\x00\x05\x03\x00\x00\
\x00\x1C\x22\x41\x00\
\x00\x41\x22\x1C\x00\
\x08\x2A\x1C\x2A\x08\
\x08\x08\x3E\x08\x08\
\x00\x50\x30\x00\x00\
\x08\x08\x08\x08\x08\
\x00\x30\x30\x00\x00\
\x20\x10\x08\x04\x02\
\x3E\x51\x49\x45\x3E\
\x00\x42\x7F\x40\x00\
\x42\x61\x51\x49\x46\
\x21\x41\x45\x4B\x31\
\x18\x14\x12\x7F\x10\
\x27\x45\x45\x45\x39\
\x3C\x4A\x49\x49\x30\
\x01\x71\x09\x05\x03\
\x36\x49\x49\x49\x36\
\x06\x49\x49\x29\x1E\
\x00\x36\x36\x00\x00\
\x00\x56\x36\x00\x00\
\x00\x08\x14\x22\x41\
\x14\x14\x14\x14\x14\
\x41\x22\x14\x08\x00\
\x02\x01\x51\x09\x06\
\x32\x49\x79\x41\x3E\
\x7E\x11\x11\x11\x7E\
\x7F\x49\x49\x49\x36\
\x3E\x41\x41\x41\x22\
\x7F\x41\x41\x22\x1C\
\x7F\x49\x49\x49\x41\
\x7F\x09\x09\x01\x01\
\x3E\x41\x41\x51\x32\
\x7F\x08\x08\x08\x7F\
\x00\x41\x7F\x41\x00\
\x20\x40\x41\x3F\x01\
\x7F\x08\x14\x22\x41\
\x7F\x40\x40\x40\x40\
\x7F\x02\x04\x02\x7F\
\x7F\x04\x08\x10\x7F\
\x3E\x41\x41\x41\x3E\
\x7F\x09\x09\x09\x06\
\x3E\x41\x51\x21\x5E\
\x7F\x09\x19\x29\x46\
\x46\x49\x49\x49\x31\
\x01\x01\x7F\x01\x01\
\x3F\x40\x40\x40\x3F\
\x1F\x20\x40\x20\x1F\
\x7F\x20\x18\x20\x7F\
\x63\x14\x08\x14\x63\
\x03\x04\x78\x04\x03\
\x61\x51\x49\x45\x43\
\x00\x00\x7F\x41\x41\
\x02\x04\x08\x10\x20\
\x41\x41\x7F\x00\x00\
\x04\x02\x01\x02\x04\
\x40\x40\x40\x40\x40\
\x00\x01\x02\x04\x00\
\x20\x54\x54\x54\x78\
\x7F\x48\x44\x44\x38\
\x38\x44\x44\x44\x20\
\x38\x44\x44\x48\x7F\
\x38\x54\x54\x54\x18\
\x08\x7E\x09\x01\x02\
\x08\x14\x54\x54\x3C\
\x7F\x08\x04\x04\x78\
\x00\x44\x7D\x40\x00\
\x20\x40\x44\x3D\x00\
\x00\x7F\x10\x28\x44\
\x00\x41\x7F\x40\x00\
\x7C\x04\x18\x04\x78\
\x7C\x08\x04\x04\x78\
\x38\x44\x44\x44\x38\
\x7C\x14\x14\x14\x08\
\x08\x14\x14\x18\x7C\
\x7C\x08\x04\x04\x08\
\x48\x54\x54\x54\x20\
\x04\x3F\x44\x40\x20\
\x3C\x40\x40\x20\x7C\
\x1C\x20\x40\x20\x1C\
\x3C\x40\x30\x40\x3C\
\x44\x28\x10\x28\x44\
\x0C\x50\x50\x50\x3C\
\x44\x64\x54\x4C\x44\
\x00\x08\x36\x41\x00\
\x00\x00\x7F\x00\x00\
\x00\x41\x36\x08\x00\
'

class Matrix8x8:
	def __init__(self, spi, cs, modules=1):
		"""
		Driver for a single MAX7219-based LED matrix.

		>>> import max7219
		>>> from machine import Pin, SPI
		>>> spi = SPI(10000000, miso=Pin(12), mosi=Pin(13), sck=Pin(14))
		>>> display = max7219.Matrix8x8(spi, Pin(2))
		>>> display.fill(True)
		>>> display.pixel(4, 4, False)
		>>> display.show()

		"""
		self.bits_horiz = 5
		self.bits_vert = 8
		self.nchars = 94
		self.monospaced = True
		div, mod = divmod(self.bits_vert, 8)
		self.bytes_vert = div if mod == 0 else div +1
		self.bytes_per_ch = self.bytes_vert * self.bits_horiz +1 if not self.monospaced else self.bytes_vert * self.bits_horiz
		self.font = _font

		self.spi = spi
		self.cs = cs
		self.cs.init(cs.OUT, True)
		self.modules = modules
		self.buffer = bytearray(8 * self.modules * 2)
		self.init()

	def init(self):
		for command, data in (
			(_SHUTDOWN, 0),
			(_DISPLAYTEST, 0),
			(_SCANLIMIT, 7),
			(_DECODEMODE, 0),
			(_SHUTDOWN, 1),
			(_INTENSITY, 0),
		):
			self.cs.low()
			for m in range(self.modules):
				self.spi.write(bytearray([command, data]))
			self.cs.high()

	def brightness(self, value):
		if not 0<= value <= 15:
			raise ValueError("Brightness out of range")
		self.cs.low()
		for m in range(self.modules):
			self.spi.write(bytearray([_INTENSITY, value]))
		self.cs.high()

	def fill(self, color):
		data = 0xff if color else 0x00
		for y in range(8 * self.modules):
			self.buffer[y] = data

	def pixel(self, x, y, color=None):
		xx = x % 8
		yy = y + int(x / 8) * 8
		if color is None:
			return bool(self.buffer[yy] & 1 << xx)
		elif color:
			self.buffer[yy] |= 1 << xx
		else:
			self.buffer[yy] &= ~(1 << xx)

	def show(self):
		for y in range(8):
			self.cs.low()
			for m in range(self.modules-1, -1, -1):
				self.spi.write(bytearray([_DIGIT0 + y, self.buffer[y + m*8]]))
			self.cs.high()

	def put_ch(self, ch, x=0):
		relch = ord(ch) -32
		if relch < 0 or relch > self.nchars:
			raise ValueError('Illegal character')
		offset = relch * self.bytes_per_ch
		bv = self.bits_vert
		bh = self.bits_horiz if self.monospaced else self.font[offset] # Char width
		offset = offset if self.monospaced else offset +1
		for bit_vert in range(bv):   # for each vertical line
			bytenum = bit_vert >> 3
			bit = 1 << (bit_vert & 0x07)        # Faster than divmod
			for bit_horiz in range(bh): #  horizontal line
				fontbyte = self.font[offset + self.bytes_vert * bit_horiz + bytenum]
				z = '*' if fontbyte & bit else ' '
				self.pixel(x + bit_horiz, self.bits_vert - bit_vert -1, (fontbyte & bit) > 0)

		return bh

	def puts(self, s, x=0):
		pos = x
		for c in s:
			pos += self.put_ch(c, pos) +1
