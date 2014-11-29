'use strict';

var gulp = require('gulp');
var mainBowerFiles = require('main-bower-files');
var less = require('gulp-less');

gulp.task('mainBowerFiles', function() {
    return gulp.src(mainBowerFiles(), {'base': 'bower_components'})
        .pipe(gulp.dest('gulp_build'));
});

gulp.task('bootstrap:prepareStaticFiles', function() {
    return gulp.src(mainBowerFiles(), {'base': 'bower_components'})
        .pipe(gulp.dest('wscales_com/zzw_theme_vertical/static'));
});

gulp.task('bootstrap:prepareLess', ['mainBowerFiles'], function() {
    return gulp.src('wscales_com/zzw_theme_vertical/less')
        .pipe(gulp.dest('gulp_build/bootstrap/less'));
});

gulp.task('bootstrap:compileLess',
    ['bootstrap:prepareLess', 'bootstrap:prepareStaticFiles'],
    function() {
        return gulp.src('gulp_build/bootstrap/less/bootstrap.less')
            .pipe(less())
            .pipe(gulp.dest(
                'wscales_com/zzw_theme_vertical/static/bootstrap/dist/css'));
    }
);

gulp.task('watch', function() {
    gulp.watch('wscales_com/zzw_theme_vertical/less/*.less',
        ['bootstrap:compileLess']);
});
