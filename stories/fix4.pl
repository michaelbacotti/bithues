#!/usr/bin/env perl
use strict;
use File::Basename;

my $dir = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/stories';
my @files = glob "$dir/*.html";

my $fixed = 0;

for my $filepath (@files) {
  my $filename = basename($filepath);
  local $/;

  open(my $fh, '<', $filepath) or die "Cannot read $filepath: $!";
  my $content = <$fh>;
  close($fh);

  my $original = $content;

  # Fix: Remove orphaned </div> that appears right after </article> before <!-- ── FOOTER ── -->
  # Also remove the extra blank line between </article> and FOOTER comment
  $content =~ s{</article>\s*\n\s*</div>\s*\n\s*(<!-- ── FOOTER ── -->)}{</article>\n\n  $1}g;

  if ($content ne $original) {
    open(my $fh, '>', $filepath) or die "Cannot write $filepath: $!";
    print $fh $content;
    close($fh);
    $fixed++;
    print "Fixed: $filename\n";
  }
}

print "\nTotal fixed: $fixed / 36\n";