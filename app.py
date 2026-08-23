from cProfile import label
import datetime
import sys
from tkinter import messagebox

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDateEdit, QDialog, QLineEdit,QPushButton,QTableWidget, QTableWidgetItem, QWidget, QMessageBox, QMainWindow
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QDate
import logica
#////////////////////////////////////////////////////////////////////////////////////////////
class MenuIU(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("MenuIU.ui", self)
        self.Clinica= logica.Clinica()
        self.regPacienteIU= RegPacienteIU()
        self.btnRegPaciente.clicked.connect(self.reg_Paciente)
        self.regServicioIU= RegServicioIU()
        self.btnRegServicio.clicked.connect(self.abrirRegServicio)
        self.regPago= RegPagoIU()
        self.btnPago.clicked.connect(self.reg_Pago)
        self.elaborarInformeIU= ElaborarInformeIU()
        self.btnInforme.clicked.connect(self.elabInforme)
        
    def reg_Paciente(self):
        self.regPacienteIU.show()
    def abrirRegServicio(self):
        self.regServicioIU.show()
    def reg_Pago(self):
        self.regPago.show()
    def elabInforme(self):
        self.elaborarInformeIU.show()
#////////////////////////////////////////////////////////////////////////////////////////////
class RegServicioIU(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Reg_ServicioIU.ui", self)
        self.Clinica= logica.Clinica()
        self.btnGuardar.clicked.connect(self.GuardarServicio)
        self.btnBuscar.clicked.connect(self.ConsultarPaciente)

    def showEvent(self, event):
        self.dFecha.setDate(QDate.currentDate())
        self.txtMonto.setText("")
        self.txtDetalle.setText("")
        self.txtCI.setText("")
        
    def ConsultarPaciente(self, CI):
        try:
            CI = int(self.txtCI.text())
            Paciente = self.Clinica.BuscarPaciente(CI)
            self.txtNomb.setText(Paciente['NombreCompleto'])
            lista = self.Clinica.cargarServicio(CI)
            self.CargarServicio(lista)
        except ValueError:
        # Se ejecutará si la conversión de CI a entero falla (por ejemplo, si el texto no es un número o no se encuentra).
            QMessageBox.critical(self, "Error", "La CI no es un número válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")

    def GuardarServicio(self):
        fech=self.dFecha.text()
        monto=self.txtMonto.text()
        detalle=self.txtDetalle.text()
        CI=self.txtCI.text()
        self.Clinica.servicio(fech, monto, detalle, CI)
        lista=self.Clinica.cargarServicio(CI)
        self.CargarServicio(lista)
        # Limpia los campos de texto después de guardar  
        self.txtNomb.clear()
        self.txtMonto.clear() 
        self.txtDetalle.clear()  
        self.txtCI.clear() 
    
    def CargarServicio(self, lista):
        filas=len(lista)
        self.lista.setRowCount(filas)
        indice=0
        for c in lista:
            self.lista.setItem(indice,0,QTableWidgetItem(str(c[0])))
            self.lista.setItem(indice,1,QTableWidgetItem(c[1]))
            self.lista.setItem(indice,2,QTableWidgetItem(str(c[2])))
            self.lista.setItem(indice,3,QTableWidgetItem(c[3]))
            self.lista.setItem(indice,4,QTableWidgetItem(str(c[4])))
            indice+=1

    def closeEvent(self, event):
        self.LimpiarCampos()

    def LimpiarCampos(self):
        self.txtNomb.clear()
        self.txtMonto.clear() 
        self.txtDetalle.clear()  
        self.txtCI.clear()
        self.LimpiarLista()

    def LimpiarLista(self):
        self.lista.setRowCount(0)
#////////////////////////////////////////////////////////////////////////////////////////////        
class ElaborarInformeIU(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.Clinica= logica.Clinica()
        uic.loadUi("InformeIU.ui", self)
        self.btnGenerar.clicked.connect(self.informe)

    def informe(self):
        self.Clinica.GenerarInforme()
        lista=self.Clinica.GenerarInforme()
        self.CargarInforme(lista)
    
    def CargarInforme(self, lista):
        filas=len(lista)
        self.lista.setRowCount(filas)
        indice=0
        for c in lista:
            self.lista.setItem(indice,0,QTableWidgetItem(str(c[0])))
            self.lista.setItem(indice,1,QTableWidgetItem(str(c[1])))
            self.lista.setItem(indice,2,QTableWidgetItem(str(c[2])))
            self.lista.setItem(indice,3,QTableWidgetItem(str(c[3])))
            self.lista.setItem(indice,4,QTableWidgetItem(str(c[4])))
            self.lista.setItem(indice,5,QTableWidgetItem(str(c[5])))
            self.lista.setItem(indice,6,QTableWidgetItem(str(c[6])))
            indice+=1
    
    def closeEvent(self, event):
        self.LimpiarLista()

    def LimpiarLista(self):
        self.lista.setRowCount(0)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class RegPacienteIU(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Reg_PacienteIU.ui", self)
        self.Clinica= logica.Clinica()
        self.btnGuardar.clicked.connect(self.GuardarPaciente)
    
    def showEvent(self, event):
        self.txtCI.setText("")
        self.txtNomb.setText("")
        self.txtTelf.setText("") 
        self.txtEda.setText("")

    def GuardarPaciente(self):
        CI = self.txtCI.text()
        nomb = self.txtNomb.text()
        telef = self.txtTelf.text()
        eda = self.txtEda.text()
    # Crear un mensaje de confirmación
        confirmacion = QMessageBox()
        confirmacion.setIcon(QMessageBox.Question)
        confirmacion.setText("¿Los datos ingresados son correctos?")
        confirmacion.setInformativeText("CI: {}\nNombre: {}\nTeléfono: {}\nEdad: {}".format(CI, nomb, telef, eda))
        confirmacion.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirmacion.setDefaultButton(QMessageBox.Ok)
    # Mostrar el mensaje y obtener la respuesta del usuario
        respuesta = confirmacion.exec_()    
    # Si el usuario da OK, guardar los datos en la base de datos y cerrar la ventana
        if respuesta == QMessageBox.Ok:
            self.Clinica.nuevoPaciente(CI, nomb, telef, eda)
        self.close()
        self.txtCI.clear()  
        self.txtNomb.clear()
        self.txtTelf.clear()
        self.txtEda.clear()  
        
    def cerrar(self):
        self.close()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class RegPagoIU(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("PagoIU.ui", self)
        self.Clinica= logica.Clinica()
        self.btnBuscar.clicked.connect(self.ConsultarPaciente)
        self.btnGuardar.clicked.connect(self.guardarMonto)
        self.btnDeuda.clicked.connect(self.Deuda)        

    def showEvent(self, event):
        self.dFecha.setDate(QDate.currentDate())
        self.txtTotal.setText("")
        self.txtCI.setText("")
        self.txtNomb.setText("")
        
    def ConsultarPaciente(self):
        try:
            CI=int(self.txtCI.text())
            paciente = self.Clinica.BuscarPaciente(CI)
            self.txtNomb.setText(paciente['NombreCompleto'])

        except ValueError:
        # Se ejecutará si la conversión de CI a entero falla (por ejemplo, si el texto no es un número o no se encuentra).
            QMessageBox.critical(self, "Error", "La CI no es un número válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}")
        
    def guardarMonto(self):
        PAGO = self.txtTotal.text()
        CI = self.txtCI.text()
        fech = self.dFecha.date().toString("yyyy-MM-dd")
        if not CI or not PAGO or not fech:
            QMessageBox.critical(self, "Error", "Debe ingresar el CI, el monto del pago y la fecha.")
            return
        
        confirmacion = QMessageBox()                                                        # Crear un mensaje de confirmación
        confirmacion.setIcon(QMessageBox.Question)
        confirmacion.setText("¿Los datos ingresados son correctos?")
        confirmacion.setInformativeText(f"CI: {CI}\nPago: {PAGO}\nFecha: {fech}")
        confirmacion.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirmacion.setDefaultButton(QMessageBox.Ok)
        
        respuesta = confirmacion.exec_()                                                     # Mostrar el mensaje y obtener la respuesta del usuario    
        if respuesta == QMessageBox.Ok:                                                      # Si el usuario da OK, guardar los datos en la base de datos y cerrar la ventana
            try:
                monto = int(PAGO)
                self.Clinica.nuevoPago(CI, monto, fech)
                QMessageBox.information(self, "Éxito", "El pago ha sido guardado correctamente.")
            except ValueError:
                QMessageBox.critical(self, "Error", "El monto debe ser un número válido.")

        self.txtTotal.clear()
#---------------------------------------------------------------------------------
    def Deuda(self):
        CI = self.txtCI.text()

        if not CI:
            QMessageBox.critical(self, "Error", "Debe ingresar el CI.")
            return
        monto = self.Clinica.mostrarMontoPendiente(CI)
        QMessageBox.information(self, "Deuda Total", "La deuda total para el CI {} es: {}".format(CI, monto))

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class loginIU(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi('LoginIU.ui', self)
        self.btnAceptar.clicked.connect(self.login)
        #self.btnCancelar.clicked.connect(self.cerrar)

    def cerrar(self):
        self.close()

    def login(self):
        usuario = self.txtUser.text()
        password = self.txtPass.text()

        if usuario == "." and password == ".":
            QMessageBox.information(self, "Inicio de sesión", "Inicio de sesión exitoso")
            self.accept()
            self.AbrirMENU()
        else:
            QMessageBox.critical(self, "Error", "Credenciales inválidas. Intente de nuevo.")
            self.txtUser.clear()
            self.txtPass.clear()

    def AbrirMENU(self):
        self.MenuIU = MenuIU()
        self.MenuIU.show()
#////////////////////////////////////////////////////////////////////////////////////////////        
def main():
    app = QApplication(sys.argv)
    login = loginIU()
    if login.exec_() == QDialog.Accepted:
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()