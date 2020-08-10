#!/usr/bin/env pwsh

$input_dir = $args[0]
$output_dir = $args[1]
$other = $args[2]


If ( $input_dir -eq $null )
{
  Write-Host "Error! Input directory not set" -ForegroundColor Red
  exit 1
}
ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Host "Error! Input directory not found" -ForegroundColor Red
  exit 1
}


If ( $output_dir -eq $null )
{
  Write-Host "Error! Output directory not set" -ForegroundColor Red
  exit 1
}


python -m pipeline.train --input $input_dir --output $output_dir $other
