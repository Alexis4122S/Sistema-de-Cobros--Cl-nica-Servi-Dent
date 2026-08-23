import sqlite3

class Clinica:
    def __init__(self):
        self.cnn=sqlite3.connect("BDPaciente.db")

    def BuscarPaciente(self, CI):
        cursor=self.cnn.execute("SELECT NombreCompleto FROM TPaciente WHERE CI = '{}'".format(CI))
        tupla = cursor.fetchone()
        return {'NombreCompleto': tupla[0]}
    
    def nuevoPaciente(self, CI, nomb, telef, Eda):
        cursor=self.cnn.execute("INSERT INTO TPaciente (CI, NombreCompleto, Telefono, Edad) VALUES('{}','{}','{}','{}')".format(CI,nomb,telef,Eda))
        self.cnn.commit()
#///////////////////////////////////////////////////////////////////////////////////////////// 
    def servicio(self, fech, monto, detalle, CI):
        cursor = self.cnn.execute("INSERT INTO TServicio (Fecha, Monto, Detalle, CI) VALUES (?, ?, ?, ?)", (fech, monto, detalle, CI))
        self.cnn.commit()

    def listarServicio(self):
        cursor=self.cnn.execute("SELECT * FROM TServicio")
        return cursor.fetchall()
    
    def cargarServicio(self, CI):
        cursor = self.cnn.execute("SELECT * FROM TServicio WHERE CI = '{}'".format (CI))
        self.cnn.commit()
        return cursor.fetchall()
#/////////////////////////////////////////////////////////////////////////////////////////////
    def nuevoPago(self, CI, Monto, fech):
        cursor=self.cnn.execute("INSERT INTO TPagos (CI, Monto, Fecha) VALUES (?, ?, ?)", (CI, Monto, fech))
        self.cnn.commit()
        
    def mostrarMontoPendiente(self, CI):
        cursor = self.cnn.execute("SELECT SUM(Monto) FROM TPagos WHERE CI = ?", (CI,))
        resultado = cursor.fetchone()
        monto = int(resultado[0]) if resultado and resultado[0] is not None else 0
        return monto - 1600
#///////////////////////////////////////////////////////////////////////////////////// 
#    def eliminarDatosServicio(self, CI):
#        cursor = self.cnn.execute("DELETE FROM TServicio WHERE CI = ?", (CI,))
#        self.cnn.commit()

    def GenerarInforme(self):
        cursor = self.cnn.execute("SELECT TPagos.CI, TPaciente.NombreCompleto, TPaciente.Edad, TPaciente.Telefono, TPagos.ID_Pago, TPagos.Fecha, TPagos.Monto FROM TPagos INNER JOIN TPaciente ON TPagos.CI = TPaciente.CI")
        return cursor.fetchall()