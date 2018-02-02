import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BusinessComponent } from 'app/business/business.component';
import { CertComponent } from 'app/cert/cert.component';
import { IssuerComponent } from 'app/issuer/issuer.component';
import { DashboardComponent } from 'app/dashboard/dashboard.component';
import { RoadmapComponent } from 'app/roadmap/roadmap.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: DashboardComponent,
    data: {
      breadcrumb: 'Search'
    }
  },
  {
    path: 'org/:orgId',
    data: {
      breadcrumb: 'Supplier Certifications'
    },
    children: [
      {
        path: '',
        component: BusinessComponent
      },
      {
        path: 'cert/:certId',
        component: CertComponent,
        data: {
          breadcrumb: 'Certification Details'
        }
      }
    ]
  },
  {
    path: 'issuer/:issuerId',
    component: IssuerComponent,
    data: {
      breadcrumb: 'Issuer Details'
    }
  },
  {
    path: 'recipe',
    redirectTo: 'recipe/start_a_restaurant'
  },
  {
    path: 'recipe/:recipeId',
    component: RoadmapComponent,
    data: {
      breadcrumb: 'Roadmap'
    }
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
