import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { VerifiableClaim, VerifiableClaimType, blankClaimType, VerifiableOrg,
  IssuerService, blankIssuerService } from '../data-types';

@Component({
  selector: 'app-cert',
  templateUrl: './cert.component.html',
  styleUrls: ['./cert.component.scss']
})
export class CertComponent implements OnInit {
  id: number;
  loaded: boolean;
  record: VerifiableClaim;
  others: VerifiableClaim[];
  props: any[];
  error: string;
  sub: any;

  constructor(
    private dataService: GeneralDataService,
    private route: ActivatedRoute) { }

  ngOnInit() {
    let loaded = this.dataService.preloadData(['inactiveclaimreasons', 'issuerservices', 'verifiableclaimtypes']);
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['certId'];
      loaded.then(status => {
        this.dataService.loadRecord('verifiableclaims', ''+this.id).subscribe((record : VerifiableClaim) => {
          let claim = this.dataService.formatClaim(record);
          let json = claim.claimJSON;
          let props = [];
          if(json && typeof json === 'string') {
            let jso = JSON.parse(json);
            if(jso) {
              for(let k in jso) {
                if((typeof jso[k] === 'number' || typeof jso[k] === 'string') && k.indexOf('_') < 0) {
                  let name = k.substring(0, 1).toUpperCase() + k.substring(1);
                  props.push({key: k, name: name, value: ''+jso[k]});
                }
              }
            }
          }
          this.props = props;
          console.log('vo claim:', claim);
          if (! claim) this.error = 'Record not found';
          else {
            this.dataService.loadVerifiableOrg(claim.verifiableOrgId)
              .subscribe((org : VerifiableOrg) => {
                console.log('org', org);
                claim.org = org;
                this.record = claim;
                if (org.claims) {
                  let others = [];
                  for (let idx = 0; idx < org.claims.length; idx++) {
                    if (org.claims[idx].claimType === claim.claimType && org.claims[idx].id !== claim.id) {
                      others.push(org.claims[idx]);
                    }
                  }
                  this.others = this.dataService.sortClaims(others);
                }
                this.loaded = !!claim;
              });
          }
        }, err => {
          this.error = err;
        });
      });
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  showVerify() {
    let div = document.getElementsByClassName('cert-verify');
    let time = 0;
    if(div.length) {
      let outer = <any>div[0];
      outer.style.display = 'block';
      let inner = outer.getElementsByClassName('verify-line');
      for(let i = 0; i < inner.length; i++) {
        let line = <any>inner[i];
        if(line.classList.contains('delay')) time += 500;
        setTimeout(() => line.classList.add('show'), time);
      }
    }
    let stat = document.getElementById('verify-status');
    if(stat) {
      setTimeout(() => (<any>stat).textContent = 'Verified', time);
    }
  }

}
