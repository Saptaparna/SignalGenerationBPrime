import sys
import ROOT as rt
import math
from LHEevent import *
from LHEfile import *
import plotTools

if __name__ == '__main__':

    #Bprime histograms
    MBPrime = rt.TH1D("MBPrime", "MBPrime", 200, 100.0, 200.0)
    MX = rt.TH1D("MX", "MX", 500, 0., 50)
    Mb = rt.TH1F("Mb", "Mb", 30, 2.0, 8.0)
    MInvariantMass_mumu = rt.TH1F("MInvariantMass_mumu", "MInvariantMass_mumu", 500, 0., 50);    
    MInvariantMass_qq = rt.TH1F("MInvariantMass_qq", "MInvariantMass_qq", 500, 0., 50.0);
    CosTheta_mumu = rt.TH1F("CosTheta_mumu", "CosTheta_mumu", 800, -4.0, 4.0); 
    MDeltaR = rt.TH1F("MDeltaR", "MDeltaR", 100, 0.0, 10.0)
    MDeltaPhi = rt.TH1F("MDeltaPhi", "MDeltaPhi", 400, -4.0, 4.0);
    mu1_lv = rt.TLorentzVector()
    mu2_lv = rt.TLorentzVector()
    q1_lv = rt.TLorentzVector()
    q2_lv = rt.TLorentzVector()

    # find events in file
    myLHEfile = LHEfile(sys.argv[1])
    myLHEfile.setMax(100000)
    eventsReadIn = myLHEfile.readEvents()
    for oneEvent in eventsReadIn:
        myLHEevent = LHEevent()
        myLHEevent.fillEvent(oneEvent)
        n_mu = 0
        n_q = 0
        for i in range(0,len(myLHEevent.Particles)):
            p = myLHEevent.Particles[i]
            if abs(p['ID'])  == 8000002: MBPrime.Fill(p['M'])
            if (abs(p['ID']) == 5 and p['M'] > 0.0): Mb.Fill(p['M'])
            if abs(p['ID'])  == 23: MX.Fill(p['M'])
            if abs(p['ID']) == 13: 
              n_mu += 1
              if n_mu==1:  mu1_lv = rt.TLorentzVector(p['Px'], p['Py'], p['Pz'], p['E'])
              if n_mu==2:  mu2_lv = rt.TLorentzVector(p['Px'], p['Py'], p['Pz'], p['E'])
              if n_mu==2:  MInvariantMass_mumu.Fill((mu1_lv+mu2_lv).M())
              if n_mu==2:  CosTheta_mumu.Fill(rt.TMath.Cos(mu1_lv.DeltaPhi(mu2_lv)))
            if ((abs(p['ID']) == 1 or abs(p['ID']) == 2 or abs(p['ID']) == 3 or abs(p['ID']) == 4)):
              n_q += 1
              if n_q==1: q1_lv = rt.TLorentzVector(p['Px'], p['Py'], p['Pz'], p['E'])
              if n_q==2: q2_lv = rt.TLorentzVector(p['Px'], p['Py'], p['Pz'], p['E'])
              if n_q==2: MInvariantMass_qq.Fill((q1_lv+q2_lv).M())
              if n_q==2: MDeltaR.Fill(q1_lv.DeltaR(q2_lv))
              if n_q==2: MDeltaPhi.Fill(q1_lv.DeltaPhi(q2_lv))
        del oneEvent, myLHEevent
        
    # write the histograms
    histoFILE = rt.TFile(sys.argv[2],"RECREATE")
    MBPrime.Write()
    MX.Write()
    Mb.Write()
    MInvariantMass_mumu.Write();
    MInvariantMass_qq.Write();
    CosTheta_mumu.Write();
    MDeltaR.Write();
    MDeltaPhi.Write();
    histoFILE.Close()
