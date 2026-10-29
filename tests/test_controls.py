"""Fault-injection tests run on disposable copies, never the original sources."""
from pathlib import Path
import sys, tempfile, shutil, unittest, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.runtime'));sys.path.insert(0,str(ROOT/'src'))
import pipeline
import pandas as pd

class Controls(unittest.TestCase):
    def setUp(self):
        (ROOT/'private').mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'private')
        self.root=Path(self.temp.name)
        shutil.copytree(ROOT/'data/raw',self.root/'data/raw')
        self.old=pipeline.ROOT;pipeline.ROOT=self.root
    def tearDown(self):
        pipeline.ROOT=self.old
        self.temp.cleanup()
    def csv(self):
        p=self.root/'data/raw'/pipeline.FILES[0];return p,pd.read_csv(p,dtype=str,keep_default_na=False)
    def test_duplicate_rejected(self):
        p,d=self.csv();pd.concat([d,d.iloc[:1]]).to_csv(p,index=False)
        with self.assertRaisesRegex(ValueError,'Duplicate'):pipeline.inspect_sources()
    def test_wrong_units_rejected(self):
        p,d=self.csv();d['UNIT_MULT']='9';d.to_csv(p,index=False)
        with self.assertRaisesRegex(ValueError,'unit contract'):pipeline.inspect_sources()
    def test_error_page_rejected(self):
        (self.root/'data/raw'/pipeline.FILES[0]).write_text('<html>Service error</html>')
        with self.assertRaisesRegex(ValueError,'HTML'):pipeline.inspect_sources()
    def test_missing_file_rejected(self):
        (self.root/'data/raw'/pipeline.FILES[0]).rename(self.root/'data/raw/absent.csv')
        with self.assertRaisesRegex(ValueError,'Missing'):pipeline.inspect_sources()
    def test_missing_quarter_not_bridged(self):
        inv,frames,w=pipeline.inspect_sources()
        frames=[d[~((d.REF_AREA=='LU')&(d.TIME_PERIOD=='2020-Q2'))].copy() for d in frames]
        _,k,_=pipeline.transform(frames,w,self.root/'candidate')
        row=k[(k.REF_AREA=='LU')&(k.TIME_PERIOD=='2020-Q3')].iloc[0]
        self.assertTrue(pd.isna(row.qoq_growth_pct));self.assertTrue(pd.isna(row.net_issuance_rate_pct))
    def test_changed_hash_retains_previous_release(self):
        inv,_,_=pipeline.inspect_sources();pipeline.save_json(self.root/'docs/data_sources/approved_source_contract.json',inv)
        pointer=self.root/'data/latest_validated.json';pointer.write_text('{"run_id":"previous-good"}')
        p,d=self.csv();d.loc[0,'OBS_VALUE']='123';d.to_csv(p,index=False)
        with self.assertRaises(SystemExit):pipeline.main()
        self.assertEqual(json.loads(pointer.read_text())['run_id'],'previous-good')

if __name__=='__main__':unittest.main(verbosity=2)
