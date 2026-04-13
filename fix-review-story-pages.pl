#!/usr/bin/perl
use strict;
use warnings;

my $BASE = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues';

sub fix_file {
    my ($file, $dir) = @_;
    my $path = "$BASE/$dir/$file";
    open(my $fh, '<', $path) or die "Cannot read $path: $!";
    my @lines = <$fh>;
    close $fh;

    my $orig = join('', @lines);

    # Detect section name
    my $sec_name = ($dir eq 'reviews') ? 'Reviews' : 'Stories';
    if ($orig =~ /Bithues\s+Reading\s+Lab\s+—\s+(Articles|Stories|Reviews)/) {
        $sec_name = $1;
    }

    # Extract full title
    my $full_title = $file;
    $full_title =~ s/\.html$//;
    if ($orig =~ /<title>([^<]+)\s+–\s+Bithues\s+Reading\s+Lab<\/title>/) {
        $full_title = $1;
    }

    # Generic hero HTML
    my $generic_hero = <<HTML;
  <section class="hero">
    <div class="hero-eyebrow">Bithues Reading Lab — $sec_name</div>
    <h1>$full_title — Bithues Reading Lab</h1>
    <p>Explore our curated insights and guides on this topic.</p>
  </section>

HTML

    my $item_type = ($dir eq 'reviews') ? 'article' : 'story';
    my $share_section = <<HTML;
        <section class="share-section">
            <h3>Share this $item_type</h3>
            <div class="share-buttons">
                <button class="share-btn" onclick="shareTwitter()">𝕏 Twitter</button>
                <button class="share-btn" onclick="shareFacebook()">📘 Facebook</button>
                <button class="share-btn" onclick="shareLinkedIn()">💼 LinkedIn</button>
            </div>
        </section>
HTML

    my @out;
    my $phase = 0; # 0=in-nav, 1=after-nav-before-hero, 2=hero-chips-article, 3=after-article
    my $in_section = 0; # 1 when inside <section class="section">
    my $done_share = 0; # prevent double injection
    my $changed = 0;

    for my $i (0 .. $#lines) {
        my $l = $lines[$i];
        my $next = ($i < $#lines) ? $lines[$i+1] : '';

        # PHASE 0: copy until </nav>
        if ($phase == 0) {
            push @out, $l;
            if ($l =~ /<\/nav>/i) { $phase = 1; }
            next;
        }

        # PHASE 1: insert generic hero before first hero
        if ($phase == 1) {
            if ($l =~ /<(?:section|header)\s+class\s*=\s*["\']hero["\'].*?>/i) {
                push @out, $generic_hero;
                $changed = 1;
            }
            push @out, $l;
            if ($l =~ /<\/(?:section|header)\s+class\s*=\s*["\']hero["\']/i) { $phase = 2; }
            next;
        }

        # PHASE 2: hero + chips + article body
        if ($phase == 2) {
            my $skip = 0;

            # Convert content-wrapper div with gradient inline style
            if ($l =~ /<div\s+class\s*=\s*["\']content-wrapper["\']\s+style\s*=\s*["\'].*?linear-gradient.*?["\'].*?>/is) {
                push @out, "  <section class=\"section\">\n";
                $in_section = 1;
                $changed = 1;
                $skip = 1;
            }
            # Convert bare <article> in stories (no class attribute)
            elsif ($l =~ /^(\s*)<article>\s*$/ && $dir eq 'stories') {
                push @out, "$1<article class=\"story\">\n";
                $changed = 1; $skip = 1;
            }
            # Convert bare </article> in stories
            elsif ($l =~ /^(\s*)<\/article>\s*$/ && $dir eq 'stories') {
                push @out, "$1</article>\n";
                $changed = 1; $skip = 1;
            }
            # Open section wrapper before article.review (if not already in section)
            elsif ($l =~ /^(\s*)<article\s+class\s*=\s*["\'](review|story)["\']/i && !$in_section) {
                push @out, "  <section class=\"section\">\n";
                $in_section = 1;
                $changed = 1;
            }
            # Close section wrapper after </article> (if in section)
            elsif ($l =~ /^(\s*)<\/article>\s*$/ && $in_section) {
                push @out, "$1</article>\n";
                push @out, "$1</section>\n";
                $in_section = 0;
                $changed = 1;
                $skip = 1;
            }
            # Convert <div class="share-section"> to <section class="share-section"> if no share section yet
            elsif ($l =~ /^(\s*)<div\s+class\s*=\s*["\']share-section["\'](.*?)>\s*$/i && !$done_share) {
                push @out, $share_section;
                $done_share = 1;
                $changed = 1;
                $skip = 1;
            }
            else {
                push @out, $l;
            }

            # Transition to phase 3 after closing article tag
            if ($l =~ /<\/article>/i) { $phase = 3; }
            next;
        }

        # PHASE 3: after article — fix share divs, skip leftover share div closes
        if ($phase == 3) {
            my $skip = 0;

            # Skip the opening <div class="share-section">
            if ($l =~ /^(\s*)<div\s+class\s*=\s*["\']share-section["\']/i) {
                $skip = 1;
            }
            # Skip opening <div class="share-buttons">
            elsif ($l =~ /^(\s*)<div\s+class\s*=\s*["\']share-buttons["\']/i) {
                $skip = 1;
            }
            # Skip closing </div> after share buttons (would close share-section div)
            elsif ($l =~ /^(\s*)<\/div>\s*$/ && $out[-1] =~ /share-btn["\']/i) {
                $skip = 1;
            }
            # Insert share section if none yet (just before footer)
            elsif ($l =~ /<footer/i && !$done_share) {
                push @out, $share_section;
                $done_share = 1;
                $changed = 1;
            }

            push @out, $l unless $skip;
            next;
        }
    }

    my $result = join('', @out);

    # Verify key elements
    my $has_gen = ($result =~ /Bithues\s+Reading\s+Lab\s+—\s+(Articles|Stories|Reviews)/);
    my $has_sec = ($result =~ /<section\s+class\s*=\s*["\x27]section["\x27]/);

    if ($has_gen && $has_sec && ($changed || $result ne $orig)) {
        open(my $fh, '>', $path) or die "Cannot write $path: $!";
        print $fh $result;
        close $fh;
        return 'fixed';
    } elsif ($result eq $orig) {
        return 'ok';
    } else {
        return "skip(gen=$has_gen sec=$has_sec changed=$changed)";
    }
}

# Process reviews
my $reviews_dir = "$BASE/reviews";
chdir $reviews_dir or die;
my @review_files = grep { /\.html$/ && !/\bfix/i } <*.html>;
my ($rf, $rk, $re) = (0, 0, 0);
for my $f (sort @review_files) {
    my $r = eval { fix_file($f, 'reviews') };
    if ($@) { warn "ERROR $f: $@"; $re++; next; }
    if ($r eq 'fixed') { print "  FIXED reviews/$f\n"; $rf++; }
    elsif ($r eq 'ok') { $rk++; }
    else { print "  SKIP reviews/$f: $r\n"; $rk++; }
}
print "Reviews: $rf fixed, $rk ok/skipped, $re errors\n";

# Process stories
my $stories_dir = "$BASE/stories";
chdir $stories_dir or die;
my @story_files = grep { /\.html$/ && !/\bfix/i } <*.html>;
my ($sf, $sk, $se) = (0, 0, 0);
for my $f (sort @story_files) {
    my $r = eval { fix_file($f, 'stories') };
    if ($@) { warn "ERROR $f: $@"; $se++; next; }
    if ($r eq 'fixed') { print "  FIXED stories/$f\n"; $sf++; }
    elsif ($r eq 'ok') { $sk++; }
    else { print "  SKIP stories/$f: $r\n"; $sk++; }
}
print "Stories: $sf fixed, $sk ok/skipped, $se errors\n";
print "TOTAL: reviews($rf fixed) stories($sf fixed)\n";
