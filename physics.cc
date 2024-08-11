#include "physics.hh"

MyPhysicsList::MyPhysicsList()
{
    RegisterPhysics (new G4EmStandardPhysics());
    RegisterPhysics (new G4OpticalPhysics());
    RegisterPhysics (new G4HadronPhysicsFTFP_BERT_TRV());
    RegisterPhysics (new G4HadronElasticPhysics());
    RegisterPhysics (new G4DecayPhysics());
}
MyPhysicsList::~MyPhysicsList()
{}
