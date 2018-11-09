import machine, micropython

class encoder:
	def __init__(self):
		self.encoderValue = 0
		self.emittedValue = 0
		self.scratch = 0

		self.pin_a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
		self.pin_b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
		self.switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
		self.disable_state = 0

		self.configure()

	def configure(self):
		encCb = self.encoderCallback
		self.pin_a.irq(trigger=machine.Pin.IRQ_RISING, handler=encCb)
		swCb = self.switchCallback
		self.switch.irq(trigger=machine.Pin.IRQ_FALLING, handler=swCb)

	def processState(self, cause):
		print("{2} - Value {0} - Switch {1}".format(self.encoderValue, self.switch.value(), cause))

		self.configure()

	def encoderCallback(self, pin):
		self.scratch = self.pin_b.value()

		self.pin_a.irq()
		self.switch.irq()

		self.encoderValue = self.encoderValue + 1 if self.scratch == 1 else -1

		try:
			micropython.schedule(self.processState, 0)
		except RuntimeError:
			pass

	def switchCallback(self, pin):
		self.pin_a.irq()
		self.switch.irq()

		try:
			micropython.schedule(self.processState, 1)
		except RuntimeError:
			pass