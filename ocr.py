import os
import ctypes

class OCR : # takes TesserArt to do OCR
	LIBPATH = "/usr/lib/libtesseract.so.3" # 
	TESSDATA_PREFIX = b'/usr/share/tesseract-ocr/tessdata' # TESSDATA_PREFIX = os.environ.get("TESSDATA_PREFIX")
	LANG = "eng" #

	def __init__(self) :
		#  load the lib
		self._lib = ctypes.cdll.LoadLibrary(self.LIBPATH)
		self._api = ctypes.c_uint64(self._lib.TessBaseAPICreate())

		#  init the engine
		if self._lib.TessBaseAPIInit3(self._api, self.TESSDATA_PREFIX, self.LANG) :
			self._lib.TessBaseAPIDelete(self._api)
			print('failed to initliaze tesserart')
			exit(3)

	def doOCR(self, filename) :
		# process the picture
		self._lib.TessBaseAPIProcessPages(self._api, filename, None, 0, None)
		self._lib.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
		text_out = self._lib.TessBaseAPIGetUTF8Text(self._api)
		
		return ctypes.string_at(text_out)


if __name__ == '__main__':
	#root, dirs, files = os.walk('.', False)
	files = os.listdir('.')
	tess = OCR()
	for fn in files:
		if fn[-3:]!='png' and fn[-3:]!='jpg' :
			continue
		print 'file[%s]: %s' % (fn, tess.doOCR(fn))
