from PyQt4 import QtCore,QtGui
import sys,threading,network_monitor,time,subprocess,ipgetter,psutil
import pyqtgraph as pg





class test_form(QtGui.QMainWindow):
    def __init__(self):
        super(test_form,self).__init__()
        self.setup_gui()
        self.widg.show()
        self.interface.currentIndexChanged.connect(self.slot_1)
        self.running = False
        self.stop_check = False


    def setup_gui(self):
        devices = psutil.net_io_counters(True)

        self.setWindowTitle("Network Monitoring App")
        self.widg = QtGui.QWidget()
        self.interface =QtGui.QComboBox(self)
        self.incoming_lbl = QtGui.QLabel("Incoming: ")
        self.outgoing_lbl = QtGui.QLabel("Outgoing: ")
        self.incoming_val = QtGui.QLabel("0")
        self.incoming_val.setStyleSheet("color: Green")
        self.incoming_metric = QtGui.QLabel("KB/s")
        self.outgoing_val = QtGui.QLabel("0")
        self.outgoing_val.setStyleSheet("color: Red")
        self.outgoing_metric = QtGui.QLabel("KB/s")
        self.total_incoming_lbl = QtGui.QLabel("Total Received: ")
        self.total_incoming_val = QtGui.QLabel("0")
        self.total_incoming_val.setStyleSheet("Color:Green")
        self.total_incoming_metric = QtGui.QLabel("KB")
        self.total_outgoing_lbl = QtGui.QLabel("Total Send: ")
        self.total_outgoing_val = QtGui.QLabel("0")
        self.total_outgoing_val.setStyleSheet("color: Red")
        self.total_outgoing_metric = QtGui.QLabel("KB")
        self.time_lbl = QtGui.QLabel("Date Time: ")
        self.time_val = QtGui.QLabel("")
        self.public_ip_lbl = QtGui.QLabel("Public IP:")
        self.public_ip_val = QtGui.QLabel("")

        self.graph = pg.GraphicsWindow()
        self.incoming_plot = self.graph.addPlot(title='Incoming')

        self.incoming_curve = self.incoming_plot.plot()
        self.outgoing_plot = self.graph.addPlot(title='Outgoing')
        self.outgoing_curve = self.outgoing_plot.plot()

        self.layout = QtGui.QHBoxLayout()
        self.graph_layout = QtGui.QVBoxLayout()
        self.label_layout = QtGui.QVBoxLayout()
        self.devices_layout = QtGui.QVBoxLayout()
        self.label_incoming = QtGui.QHBoxLayout()
        self.label_outgoing = QtGui.QHBoxLayout()
        self.label_total_incoming = QtGui.QHBoxLayout()
        self.label_total_outgoing = QtGui.QHBoxLayout()
        self.label_time = QtGui.QHBoxLayout()
        self.label_public_ip = QtGui.QHBoxLayout()

        self.label_layout.addLayout(self.devices_layout)
        self.label_layout.addLayout(self.label_incoming)
        self.label_layout.addLayout(self.label_outgoing)
        self.label_layout.addLayout(self.label_total_incoming)
        self.label_layout.addLayout(self.label_total_outgoing)
        self.label_layout.addLayout(self.label_time)
        self.label_layout.addLayout(self.label_public_ip)
        
        
        self.label_layout.setAlignment(QtCore.Qt.AlignTop)

        self.layout.addLayout(self.graph_layout)
        self.layout.addLayout(self.label_layout)

        self.widg.setLayout(self.layout)
        self.devices_layout.addWidget(self.interface)
        self.label_incoming.addWidget(self.incoming_lbl)
        self.label_incoming.addWidget(self.incoming_val)
        self.label_incoming.addWidget(self.incoming_metric)
        self.label_outgoing.addWidget(self.outgoing_lbl)
        self.label_outgoing.addWidget(self.outgoing_val)
        self.label_outgoing.addWidget(self.outgoing_metric)
        self.label_total_incoming.addWidget(self.total_incoming_lbl)
        self.label_total_incoming.addWidget(self.total_incoming_val)
        self.label_total_incoming.addWidget(self.total_incoming_metric)
        self.label_total_outgoing.addWidget(self.total_outgoing_lbl)
        self.label_total_outgoing.addWidget(self.total_outgoing_val)
        self.label_total_outgoing.addWidget(self.total_outgoing_metric)
        self.label_time.addWidget(self.time_lbl)
        self.label_time.addWidget(self.time_val)
        self.label_public_ip.addWidget(self.public_ip_lbl)
        self.label_public_ip.addWidget(self.public_ip_val)
        self.graph_layout.addWidget(self.graph)
        for dev in devices:
            self.interface.addItem(dev)

    def slot_1(self):

        self.interface_choice(self.interface.currentText())

    def interface_choice(self,interface_val):

        self.start_time = time.time()
        if  self.running:

            self.stop_check = True
            time.sleep(1)
            self.check_thread = threading.Thread(target=self.run_check,args=(interface_val,) ,daemon=True)
            self.stop_check = False
            self.check_thread.start()

        else:

            self.check_thread = threading.Thread(target=self.run_check,args=(interface_val,) ,daemon=True)
            self.check_thread.start()
            self.running = True
            
        
        check_ip = threading.Thread(target=self.find_ip,daemon=True)
        check_ip.start()

    def run_check(self,interface_val):

        self.bytes_recv = 0
        self.bytes_sent = 0
        self.prev_val = []
        self.incoming_list = []
        self.outgoing_list = []
        self.time = []


        while True:


            if self.stop_check == True:

                break
                
            self.current_time = time.time()-self.start_time
            self.val = network_monitor.collect_data(interface_val)
            self.val_lst = self.val.split(":")
            if not self.prev_val:

                pass

            else:
                self.time.append(self.current_time)

                self.bytes_recv = float(self.val_lst[0]) - float(self.prev_val[0])
                self.incoming_list.append(int(self.bytes_recv))
                self.bytes_recv_val,self.bytes_recv_lbl = self.Determine_Label(self.bytes_recv)


                self.bytes_sent = float(self.val_lst[1]) - float(self.prev_val[1])
                self.outgoing_list.append(int(self.bytes_sent))
                self.bytes_sent_val, self.bytes_sent_lbl = self.Determine_Label(self.bytes_sent)

                if self.bytes_recv < 0:

                    self.bytes_recv = 0

                if self.bytes_sent < 0:

                    self.bytes_sent = 0

                self.incoming_val.setText(str(self.bytes_recv_val))
                self.incoming_metric.setText(self.bytes_recv_lbl +"/s")
                self.outgoing_val.setText(str(self.bytes_sent_val))
                self.outgoing_metric.setText(self.bytes_sent_lbl+"/s")

            self.prev_val = self.val_lst

            print("Time: "+str(round(self.current_time,2)) +"\tIncoming: "+str(round(self.bytes_recv,2))+"\tOutgoing: "+str(round(self.bytes_sent,2)))

            self.incoming_curve.setData(self.time,self.incoming_list,pen='g')
            self.outgoing_curve.setData(self.time,self.outgoing_list,pen='r')
            self.find_total()
            


    def find_total(self):
        
        latest = subprocess.check_output("tail -1 stats.csv",shell=True)
        result_list = latest.decode('utf-8').split(",")
        time = result_list[2]

        self.total_incoming_mod,self.total_incoming_power = self.Determine_Label(result_list[0])
        self.total_outgoing_mod, self.total_outgoing_power = self.Determine_Label(result_list[1])

        self.total_incoming_val.setText(str(self.total_incoming_mod))
        self.total_incoming_metric.setText(self.total_incoming_power)

        self.total_outgoing_val.setText(str(self.total_outgoing_mod))
        self.total_outgoing_metric.setText(self.total_outgoing_power)

        self.time_val.setText(time[:19])


    def find_ip(self):
        
        self.external_ip = ipgetter.myip()
        self.public_ip_val.setText(self.external_ip)
        time.sleep(300)

        
    def Determine_Label(self,val):

        val = float(val)

        if (val / 1000000000) >= 1:
            return str(round((val/1000000000),2)),"GB"

        elif (val / 1000000) >= 1:
            return str(round((val/1000000),2)),"MB"

        elif (val/1000) >=1 :
            return str(round(val/1000,2)),"KB"

        else:
            return str(round(val,2)),"B"






app = QtGui.QApplication(sys.argv)
window = test_form()
sys.exit(app.exec_())

