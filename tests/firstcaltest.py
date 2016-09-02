import unittest
import capo, aipy as a, numpy as np, pylab as p, os

class TestFirstCal(unittest.TestCase):
    @classmethod
    def setUpClass(self):
<<<<<<< HEAD
        #testdata_path='/Users/sherlock/src/capo/tests/data/'
        testdata_path='/home/zakiali/src/mycapo/tests/data/'
=======
        testdata_path='/home/saulkohn/tests/'
>>>>>>> 844339aa7de103571bb31f86b34a3ebe792ded92
        #True delays put into simulated data
        self.true = np.load(testdata_path+'truedelays.npz')
        #solved firstcal delays
        self.solved = np.load(testdata_path+'zen.2457458.32700.xx.uvAs.npz')
        #raw data used to solve for the first cal solutions
        self.raw_data = [testdata_path+'zen.2457458.32700.xx.uvAs']
        aa = a.cal.get_aa('hsa7458_v000_HH_delaytest', np.array([.150]))
        self.info = capo.omni.aa_to_info(aa, fcal=True)
        self.reds = self.info.get_reds()
        self.fqs = np.linspace(.1,.2,1024)  
        self.pol = 'xx'
        #Get raw data
        reds = capo.zsa.flatten_reds(self.reds)
        ant_string =','.join(map(str,self.info.subsetant))
        bl_string = ','.join(['_'.join(map(str,k)) for k in reds])
        times, data, flags = capo.arp.get_dict_of_uv_data(self.raw_data, bl_string, 'xx', verbose=True)
        self.dataxx = {}
        self.wgtsxx = {}
        for (i,j) in data.keys():
            self.dataxx[(i,j)] = data[(i,j)]['xx']#[0:1,:]
            self.wgtsxx[(i,j)] = np.logical_not(flags[(i,j)]['xx'])#[0:1,:])


    def test_run_firstcal(self):
        fc = capo.omni.FirstCal(self.dataxx,self.wgtsxx,self.fqs,self.info)
        sols = fc.run(tune=True,verbose=False,offset=True,plot=False)
        capo.omni.save_gains_fc(sols,self.fqs,self.pol,filename=self.raw_data,ubls=' ',ex_ants=[],verbose=True)
        assert(os.path.exists(self.raw_data[0]+'.fc.npz'))
        npzdata = np.load(self.raw_data[0]+'.fc.npz') 
        for k in ['cmd','ubls','ex_ants']: assert(k in npzdata.keys())
        for k in npzdata.keys():
            if k.isdigit():
                assert(str(k)+'d' in npzdata.keys())
    def test_plot_redundant(self):
        reds2plot = self.reds[3] #random set of redundant baseliens
        time = 13
        for bl in reds2plot:
            try:
                a1,a2 = bl
                p.subplot(211)
                p.plot(self.fqs, np.angle(self.dataxx[bl][time]))
                p.subplot(212)
                p.plot(self.fqs, np.angle( self.dataxx[bl][time]*np.conj(self.solved[str(a1)])*self.solved[str(a2)] ))
            except (KeyError):
                bl = bl[::-1]
                a1,a2 = bl
                p.subplot(211)
                p.plot(self.fqs, np.angle(self.dataxx[bl][time]))
                p.subplot(212)
                p.plot(self.fqs, np.angle( self.dataxx[bl][time]*np.conj(self.solved[str(a1)])*self.solved[str(a2)] ))
        p.show() 

    def test_redundancy(self):
        reds = [('d'+str(i),'d'+str(j)) for i,j in self.reds[3]]
        i0,i1 = reds[0] #fist baseline in the reds[3] redundant bl list
        t0 = self.true[i0]
        t1 = self.true[i1]
        tp0, tp1 = self.solved[i0], self.solved[i1]
        delays = []
        for (a0,a1) in reds:
            t2,t3 = self.true[a0], self.true[a1]
            t3 = self.true[a1]
            tp2, tp3 = self.solved[a0], self.solved[a1]
            delays.append(np.abs( (t0 - tp0) - (t1 - tp1) - ((t2 - tp2) - (t3-tp3)) ) )
        zero = np.zeros_like(delays)
        for k in delays:
            self.assertAlmostEquals(k, 0.0, delta=.1) 

unittest.main()
