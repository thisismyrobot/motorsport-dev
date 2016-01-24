#rem

notes
-----

 - 100% duty would be nice to be 200kph
 - 100% duty (8mhz clock) @ 10khz = 200kph = pwmout 2,199,800
    
 - example string: $GPVTG,270.0,T,,,0.0,N,0.0,K,A*45
  
#endrem

setup:
    'overclock :)
    setfreq m8

    symbol KPH = b1
    symbol PWM_VAL = w1

    'set calib to 100kph
    pwmout 2,199,400

    'turn on led to inidicate starting serial comms
    high 1

    'wait for any gps data
    serin 4,T2400,("$GP")

    'turn off led to confirm serial comms
    low 1

lock:

    'wait for lock
    serin 4,T2400,("A*")

main:

get_gpvgt:

    serin 4,T2400,("$GP"),b0
    if b0 != 86 then' "V"
        goto get_gpvgt
    endif

    'the "N," is just before what (the kph)
    serin 4,T2400,("N,"),#KPH

    'toggle LED to conf working
    toggle 1

    'display on voltmeter using pwm
    PWM_VAL = KPH * 4

    'set to zero if less the 5kph
    if PWM_VAL < 20 then
        pwmout 2,0,0
        low 2
    else
        pwmout 2,199,PWM_VAL
    endif

    goto main







