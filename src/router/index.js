import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminloginView from "../views/AdminloginView.vue";
import SignupView from "../views/SignupView.vue";
import UserloginView from "../views/UserloginView.vue";
import CreatorloginView from "../views/CreatorloginView.vue";
import CreatordashboardView from "../views/CreatordashboardView.vue";
import UserdashboardView from "../views/UserdashboardView.vue";
import UserviewsongView from "../views/UserviewsongView.vue";
import UserplaylistView from "../views/UserplaylistView.vue";
import AdmindashboardView from "../views/AdmindashboardView.vue";
import UpdatealbumView from "../views/UpdatealbumView.vue";
import UpdatesongView from "../views/UpdatesongView.vue";
import UserprofileView from "../views/UserprofileView.vue";
import CreatorviewsongView from "../views/CreatorviewsongView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/adminlogin",
    name: "adminlogin",
    component: AdminloginView,
  },
  {
    path: "/signup",
    name: "signup",
    component: SignupView,
  },
  {
    path: "/userlogin",
    name: "userlogin",
    component: UserloginView,
  },
  {
    path: "/creatorlogin",
    name: "creatorlogin",
    component: CreatorloginView,
  },
  {
    path: "/creatordashboard",
    name: "creatordashboard",
    component: CreatordashboardView,
  },
  {
    path: "/userdashboard",
    name: "userdashboard",
    component: UserdashboardView,
  },
  {
    path: "/userviewsong/:song_id",
    name: "userviewsong",
    component: UserviewsongView,
  },
  {
    path: "/userplaylist/:user_id",
    name: "userplaylist",
    component: UserplaylistView,
  },
  {
    path: "/admindashboard",
    name: "admindashboard",
    component: AdmindashboardView,
  },
  {
    path: "/userprofileview",
    name: "userprofileview",
    component: UserprofileView,
  },
  {
    path: "/updatesong/:songId",
    name: "updatesong",
    component: UpdatesongView,
  },
  {
    path: "/updatealbum/:albumId",
    name: "updatealbum",
    component: UpdatealbumView,
  },
  {
    path: "/creatorviewsong",
    name: "creatorviewsong",
    component: CreatorviewsongView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ "../views/AboutView.vue");
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
