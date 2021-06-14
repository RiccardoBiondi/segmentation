#!/usr/bin/env pwsh

[CmdletBinding()]
Param
(
  [parameter(mandatory=$true, position=0)][string]$input_dir,
  [parameter(mandatory=$true, position=1)][string]$output_dir
)


If ( $null -eq $input_dir)
{
  Write-Error -Message "Error! Input directory not set" -Category NotSpecified -RecommendedAction "Set a path to the input directory"
  exit 1
}

ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Error -Message "Error! Input directory not found" -Category ObjectNotFound
  exit 1
}


If ( $null -eq $output_dir)
{
  Write-Error -Message "Error! Output directory not set" -Category NotSpecified -RecommendedAction "Set a path t the output directory"
  exit 1
}

ElseIf ( -not (Test-Path -Path $output_dir -PathType Container) )
{
  Write-Error -Message "Error! Output directory not found" -Category ObjectNotFound
  exit 1
}

python -m CTLungSeg.train --input $input_dir --output $output_dir $args[2..$args.Length]
