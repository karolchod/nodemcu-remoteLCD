#Library that can be used in python projects using remoteLCD device
import socket
import time


class SimpleLCD():

    ### PRIVATE METHODS ###
    def __init__(self):

        self.ip_addr = "192.168.100.100" #Please enter device IP address
        self.port = 4210
        self.opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __removeAccents(self,
                        input_text):  # based on https://gist.github.com/AdoHaha/a76157c6de5155bf6b0adc77988724d9, added ’ to ' which was shown as beta in arduino, maybe will find other problems with LCD and add them here
        # strange = 'ĄąĆćĘęŁłŃńÓóŚśŹźŻż'
        # ascii_replacements = 'AaCcEeLlNnOoSsZzZz' # only polish letters
        strange = 'ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ’'
        ascii_replacements = 'UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht\''
        translator = str.maketrans(strange, ascii_replacements)
        return input_text.translate(translator)

    # METHODS FOR OUTSIDE USE###
    def send(self, row, text):
        if row == 0 or row == 1:
            # time.sleep(1)
            text = self.__removeAccents(text)
            # self.s.write((str(row) + text[0:16] + '\n').encode())
            byte_message = bytes(str(row)+text, "utf-8")
            # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
            print("sent: " + str(row) + text[0:16])
            # time.sleep(1.5)

    def scroll(self, row, text):
        if row == 0:
            # time.sleep(1.5)
            text = self.__removeAccents(text)
            # self.s.write(("2" + text + '\n').encode())
            byte_message = bytes("2"+text, "utf-8")
            # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
            print("sent: " + "2" + text)
            # time.sleep(1.5)
        elif row == 1:
            # time.sleep(1.5)
            text = self.__removeAccents(text)
            # self.s.write(("3" + text + '\n').encode())
            byte_message = bytes("3" + text, "utf-8")
            # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
            print("sent: " + "3" + text)
            # time.sleep(1.5)

    def beep(self, times):
        if 1 <= times <= 9:
            # self.s.write(("6" + str(times) + '\n').encode())
            byte_message = bytes("6", "utf-8")
            # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
            # time.sleep(1)
            print("beep " + str(times) + " times")
        else:
            print("wrong number")

    def backlight_on(self):
        # self.s.write(("7" + '\n').encode())
        byte_message = bytes("7", "utf-8")
        # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
        # time.sleep(1)
        print("backlight on")

    def backlight_off(self):
        # self.s.write(("8" + '\n').encode())
        byte_message = bytes("8", "utf-8")
        # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
        # time.sleep(1)
        print("backlight off")

    def clear(self):
        # time.sleep(0)
        # self.s.write(("9" + '\n').encode())
        byte_message = bytes("9", "utf-8")
        # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
        # time.sleep(1.5)
        print("sent: 9")
        
    def clock(self):
        # time.sleep(0)
        # self.s.write(("9" + '\n').encode())
        byte_message = bytes("5", "utf-8")
        # opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.opened_socket.sendto(byte_message, (self.ip_addr, self.port))
        # time.sleep(1.5)
        print("sent: 5")

    def __del__(self):
        # time.sleep(2)
        # self.s.reset_input_buffer()
        # self.s.reset_output_buffer()
        # self.s.close()
        self.opened_socket.shutdown(socket.SHUT_RDWR)
        self.opened_socket.close()
        print("~~Disconnected")
