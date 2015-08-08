from RPIO import PWM
import wiringpi2 as wiringpi
import time

servo = PWM.Servo()

class MotorObject(object):

    def __init__(self):

        self.period = 2000 #microseconds

        #define GPIO number
        self.motor_left_A =  7
        self.motor_left_B =  8
        self.motor_right_A =  9
        self.motor_right_B = 10

        #GPIO init
        wiringpi.wiringPiSetupGpio()

        #Sets GPIO to output
        wiringpi.pinMode(self.motor_left_A, 1)
        wiringpi.pinMode(self.motor_left_B, 1)
        wiringpi.pinMode(self.motor_right_A, 1)
        wiringpi.pinMode(self.motor_right_B, 1)

        #Create PWM
        wiringpi.softPwmCreate(self.motor_left_A,0,100)
        wiringpi.softPwmCreate(self.motor_left_B,0,100)
        wiringpi.softPwmCreate(self.motor_right_A,0,100)
        wiringpi.softPwmCreate(self.motor_right_B,0,100)

    def stop(self):
        wiringpi.softPwmWrite(self.motor_left_A,0)
        wiringpi.softPwmWrite(self.motor_left_B,0)
        wiringpi.softPwmWrite(self.motor_right_A,0)
        wiringpi.softPwmWrite(self.motor_right_B,0)

    def forward(self,dutycycle):
        wiringpi.digitalWrite(self.motor_left_B, 0)
        wiringpi.digitalWrite(self.motor_right_B, 0)
        wiringpi.softPwmWrite(self.motor_left_A,dutycycle)
        wiringpi.softPwmWrite(self.motor_right_A,dutycycle-5)

    def backward(self,dutycycle):
        wiringpi.digitalWrite(self.motor_left_A, 0)
        wiringpi.digitalWrite(self.motor_right_A, 0)
        wiringpi.softPwmWrite(self.motor_left_B,dutycycle)
        wiringpi.softPwmWrite(self.motor_right_B,dutycycle)

class UltraSonicObject(object):

    def __init__(self):
        self.time_scan_time = 0.06 #seconds

        #define GPIO number
        self.trig_pin = 2
        self.echo_pin = 3

        #GPIO init
        wiringpi.wiringPiSetupGpio()

        #Sets GPIO to output
        wiringpi.pinMode(self.trig_pin, 1)
        #Reset Output
        wiringpi.digitalWrite(self.trig_pin, 0)

        #Sets GPIO to input
        wiringpi.pinMode(self.echo_pin, 0)

    def trigger(self):
        # Short LOW pulse to produce clean 10us HIGH pulse
        wiringpi.digitalWrite(self.trig_pin, 0)
        wiringpi.delayMicroseconds(5)
        wiringpi.digitalWrite(self.trig_pin, 1)
        wiringpi.delayMicroseconds(15)
        wiringpi.digitalWrite(self.trig_pin, 0)

    def echo(self):
        pulse_start = 0
        pulse_end = 0

        while wiringpi.digitalRead(self.echo_pin) == 0:
            pulse_start = time.time()

        while wiringpi.digitalRead(self.echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        return pulse_duration

    def measure(self):
        self.trigger()
        echo_time = self.echo()
        distance = round(echo_time * 17150, 2)
        return distance

class ServoMotorObject(object):

    def __init__(self):
        #define GPIO number
        self.servomotor =  18

    def rotate(self,angle):
        pulse = round(9.9755*angle + 185,-1)
        servo.set_servo(self.servomotor, int(pulse))
        time.sleep(0.4)
        servo.stop_servo(self.servomotor)

def main():
    motor_obj = MotorObject()
    ultrasonic_obj = UltraSonicObject()
    servomotor_obj = ServoMotorObject()

    distance = ultrasonic_obj.measure()
    scan_num = 50
    scan = scan_num

    servomotor_obj.rotate(90)


    while 1:

        if ultrasonic_obj.measure() < 35:
            motor_obj.forward(0)
            time.sleep(0.1)

        elif ultrasonic_obj.measure() >= 35:
            motor_obj.forward(40)
            time.sleep(0.1)

if __name__ == "__main__":
    main()
