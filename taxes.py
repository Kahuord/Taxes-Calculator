#как перевести Брутто ежемесячную зарплату в Нетто
podohod_nalog_salary = 1667
min_salary = 620
sos_nalog = 0.105
sos_nalog_rabotafatel = 0.2359
poslina_riska_rabotofatela = 0.36
#calculate_salary(2000)

def calculate_salary_izv_voz_inv(salary,izv,voz,inv):
    izv_nolog = 0.1
    sos_nalog = 0.1
    sos_nalog_rabotafatel = 0.1
    inv_nalog = 0.1
    nalog_s_summi_boljshe_1667 = 0.1
    nalog_s_summi_1667 = 0.1

    izv_nolog = izv*250

    if voz == 0:
        sos_nalog = 0.105
        sos_nalog_rabotafatel = 0.2359
    elif voz == 1:
        sos_nalog = 0.0976
        sos_nalog_rabotafatel = 0.2194
    elif voz == 2:
        sos_nalog = 0.0925
        sos_nalog_rabotafatel = 0.2077

    if inv == 0:
        inv_nalog = 0
    elif inv == 1 or 2:
        inv_nalog = 154
    elif inv == 3:
        inv_nalog = 120


    salary_sos_nalog = salary * sos_nalog
    if salary <= podohod_nalog_salary:
        podohod_nalog = 0.23
        nalog_s_summi_boljshe_1667 = 0
        a = salary - salary_sos_nalog - izv_nolog - inv_nalog
        a = ((a*a)**(1/2)+a)/2
    elif salary > podohod_nalog_salary:
        podohod_nalog = 0.2
        a = podohod_nalog_salary - salary_sos_nalog - izv_nolog - inv_nalog
        a = ((a * a) ** (1 / 2) + a) / 2
        nalog_s_summi_boljshe_1667 = (salary - podohod_nalog_salary) * 0.23

    nalog_s_summi_1667 = a * podohod_nalog
    nalog_rabotofatela = salary * sos_nalog_rabotafatel
    rabotofatel_platit = salary * (1 + sos_nalog_rabotafatel) + poslina_riska_rabotofatela
    salary_Netto = salary-salary_sos_nalog-nalog_s_summi_1667-nalog_s_summi_boljshe_1667
    return salary_Netto

    #print("sos nalog - ", salary_sos_nalog)
    #print("nalog s summi 1667 - ", nalog_s_summi_1667)
    #print("nalog s summi boljshe 1667 - ", nalog_s_summi_boljshe_1667)
    #print("nalog rabotofatela - ", nalog_rabotofatela)
    #print("rabotofatel platit - ", rabotofatel_platit)
    #print("Brutto zarplata - ", salary)
    #print("Netto zarplata - ", salary_Netto)
    #print('')
    #print(izv_nolog, '', inv_nalog)
#Net Pensii - 0
#Pensija po visluge - 1
#Pensija po vozvrastu - 2
calculate_salary_izv_voz_inv(2000,10,0,0)