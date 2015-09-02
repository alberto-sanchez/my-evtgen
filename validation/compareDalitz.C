void compareDalitz(TString name1, TString name2, TString save="") {
  TCanvas c1;
  c1.Divide(2,2);
  TFile f1(name1);
  TFile f2(name2);
  TTree* t1 = (TTree*)f1.Get("dalitzTree");
  TTree* t2 = (TTree*)f2.Get("dalitzTree");
  t1->SetMarkerColor(kRed);
  t1->SetLineColor(kRed);
  t2->SetMarkerColor(kBlue);
  t2->SetLineColor(kBlue);
  gStyle->SetOptStat(0);
  c1.cd(1);
  t1->Draw("invMass12:invMass23","");
  t2->Draw("invMass12:invMass23","","same");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetTitle("");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetXTitle("Mass 23 [GeV/c^{2}]");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetYTitle("Mass 12 [GeV/c^{2}]");
  c1.cd(2);
  t1->Draw("invMass12","");
  t2->Draw("invMass12","","same");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetTitle("");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetXTitle("Mass 12 [GeV/c^{2}]");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetYTitle("");
  c1.cd(3);
  t1->Draw("invMass23","");
  t2->Draw("invMass23","","same");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetTitle("");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetXTitle("Mass 23 [GeV/c^{2}]");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetYTitle("");
  c1.cd(4);
  t1->Draw("invMass13","");
  t2->Draw("invMass13","","same");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetTitle("");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetXTitle("Mass 13 [GeV/c^{2}]");
  ((TH1F*)gPad->GetPrimitive("htemp"))->SetYTitle("");
  c1.Update();

  if(save!="") {
    c1.SaveAs(save+".png");
  } else {
    cout <<"Hit Enter to continue"<<endl;
    while (getchar() != '\n');
  }
}
