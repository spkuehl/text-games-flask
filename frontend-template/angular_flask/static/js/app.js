'use strict';

angular.module('AngularFlask', ['angularFlaskServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/landing.html',
			controller: IndexController
		})
		.when('/about', {
			templateUrl: 'static/partials/about.html',
			controller: AboutController
		})
		.when('/post', {
			templateUrl: 'static/partials/post-list.html',
			controller: PostListController
		})
		.when('/post/:postId', {
			templateUrl: '/static/partials/post-detail.html',
			controller: PostDetailController
		})
		/* Create a "/blog" route that takes the user to the same place as "/post" */
		.when('/join', {
			templateUrl: 'static/partials/join.html',
			controller: PostListController
		})
		.when('/lobby', {
			templateUrl: 'static/partials/lobby.html',
			controller: PostListController
		})
		.when('/waiting', {
			templateUrl: 'static/partials/waiting.html',
			controller: PostListController
		})
		.when('/voting', {
			templateUrl: 'static/partials/voting.html',
			controller: PostListController
		})
		.when('/dasher', {
			templateUrl: 'static/partials/dasher.html',
			controller: PostListController
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);
	}])
;
